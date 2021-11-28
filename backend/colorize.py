import cv2 as cv
import numpy as np
import grpc
import tensorflow as tf
from tensorflow import make_tensor_proto, make_ndarray
from tensorflow_serving.apis import prediction_service_pb2_grpc, predict_pb2
from helpers import get_model_metadata


def convert_to_opencv(file, cv2_img_flag=cv.IMREAD_ANYCOLOR):
    img_array = np.asarray(bytearray(file.read()), dtype=np.uint8)
    return cv.imdecode(img_array, cv2_img_flag)


def convert_to_bytes(open_cv_img):
    _, buffer = cv.imencode('.jpg', open_cv_img)
    return buffer.tobytes()


def colorize_image(file, model):
    original_frame = convert_to_opencv(file)

    (h_orig, w_orig) = original_frame.shape[:2]

    address = "{}:{}".format(model[0], model[1])

    channel = grpc.insecure_channel(address)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    model_name = 'colorization-v2'

    input_metadata, output_metadata = get_model_metadata(stub, model_name)
    input_shape = input_metadata['data_l']['shape']

    output_shape = output_metadata['color_ab']['shape']
    _, _, h_in, w_in = input_shape
    print('input shape', original_frame.shape)

    if original_frame.shape[2] > 1:
        frame = cv.cvtColor(cv.cvtColor(
            original_frame, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2RGB)
    else:
        frame = cv.cvtColor(original_frame, cv.COLOR_GRAY2RGB)

    img_rgb = frame.astype(np.float32) / 255
    img_lab = cv.cvtColor(img_rgb, cv.COLOR_RGB2Lab)
    img_l_rs = cv.resize(img_lab.copy(), (w_in, h_in))[:, :, 0]

    batch_size = 1

    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name

    for input_name in input_metadata:
        request.inputs[input_name].CopyFrom(make_tensor_proto(
            np.zeros(input_metadata[input_name]['shape']), dtype=tf.dtypes.float32))

    request.inputs['data_l'].CopyFrom(
        make_tensor_proto(img_l_rs, shape=(1, 1, 256, 256)))
    # result includes a dictionary with all model outputs
    result = stub.Predict(request, 10.0)

    if 'color_ab' not in result.outputs:
        print("Available outputs:")
        for Y in result.outputs:
            print(Y)
        exit(1)

    res = make_ndarray(result.outputs['color_ab'])

    update_res = np.squeeze(res)

    out = update_res.transpose((1, 2, 0))
    out = cv.resize(out, (w_orig, h_orig))
    img_lab_out = np.concatenate(
        (img_lab[:, :, 0][:, :, np.newaxis], out), axis=2)
    img_bgr_out = np.clip(cv.cvtColor(
        img_lab_out, cv.COLOR_Lab2BGR), 0, 1) * 255

    return convert_to_bytes(img_bgr_out)
