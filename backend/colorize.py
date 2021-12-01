import os 

import cv2 as cv
import grpc
import numpy as np
import tensorflow as tf

from tensorflow import make_ndarray, make_tensor_proto
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

from helpers import get_model_metadata


def convert_to_opencv(file, cv2_img_flag=cv.IMREAD_ANYCOLOR):
    img_array = np.asarray(bytearray(file.read()), dtype=np.uint8)
    return cv.imdecode(img_array, cv2_img_flag)


def convert_to_bytes(open_cv_img):
    _, buffer = cv.imencode('.jpg', open_cv_img)
    return buffer.tobytes()


def connect_grpc_model(address=os.getenv("GRPC_ADDRESS", '127.0.0.1'), port=os.getenv("GRPC_PORT", '9001')):
    address = "{}:{}".format(address, port)
    channel = grpc.insecure_channel(address)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    return stub


def prep_model_input(remote_model, model_name):
    input_metadata, _ = get_model_metadata(remote_model, model_name)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name
    for input_name in input_metadata:
        request.inputs[input_name].CopyFrom(make_tensor_proto(
            np.zeros(input_metadata[input_name]['shape']), dtype=tf.dtypes.float32))
    input_shape = input_metadata['data_l']['shape']
    return (request, input_shape)


def transform_to_grayscale(original_frame):
    if original_frame.shape[2] > 1:
        return cv.cvtColor(cv.cvtColor(
            original_frame, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2RGB)
    return cv.cvtColor(original_frame, cv.COLOR_GRAY2RGB)


def transform_to_normal_lab(img_rgb):
    return cv.cvtColor(img_rgb.astype(np.float32) / 255, cv.COLOR_RGB2Lab)


def predict_result(request, remote_model):
    result = remote_model.Predict(request, 10.0)
    if 'color_ab' not in result.outputs:
        print("Available outputs:")
        for Y in result.outputs:
            print(Y)
        exit(1)
    res = make_ndarray(result.outputs['color_ab'])
    update_res = np.squeeze(res)
    return update_res.transpose((1, 2, 0))


def colorize_image(file, model_name):
    original_frame = convert_to_opencv(file)
    (h_orig, w_orig) = original_frame.shape[:2]

    # connect to the remote AI/ML model
    remote_model = connect_grpc_model()
    (request, input_shape) = prep_model_input(remote_model, model_name)

    # transform image to grayscale LAB and input size
    h_in, w_in = input_shape[2:4]
    gray_frame = transform_to_grayscale(original_frame)
    img_lab = transform_to_normal_lab(gray_frame)
    img_l_rs = cv.resize(img_lab.copy(), (w_in, h_in))[:, :, 0]

    # send input image to model
    request.inputs['data_l'].CopyFrom(
        make_tensor_proto(img_l_rs, shape=input_shape))
    result = predict_result(request, remote_model)

    # resize predicted color pixels to original image
    out = cv.resize(result, (w_orig, h_orig))
    # combine original Light info with predicted colors info
    img_lab_out = np.concatenate(
        (img_lab[:, :, 0][:, :, np.newaxis], out), axis=2)
    # back to RGB and 255-scale
    img_bgr_out = np.clip(cv.cvtColor(
        img_lab_out, cv.COLOR_Lab2BGR), 0, 1) * 255

    return convert_to_bytes(img_bgr_out)
