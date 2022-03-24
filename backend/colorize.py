import os 

import cv2 as cv
import numpy as np

from ovmsclient import make_grpc_client, make_tensor_proto


def convert_to_opencv(file, cv2_img_flag=cv.IMREAD_ANYCOLOR):
    img_array = np.asarray(bytearray(file.read()), dtype=np.uint8)
    return cv.imdecode(img_array, cv2_img_flag)


def convert_to_bytes(open_cv_img):
    _, buffer = cv.imencode('.jpg', open_cv_img)
    return buffer.tobytes()


def prep_model_input(model_metadata):
    inputs = {}
    input_metadata = model_metadata["inputs"]
    for input_name in input_metadata:
        inputs[input_name] = np.zeros(input_metadata[input_name]['shape'], dtype=np.float32)
    input_shape = input_metadata['data_l']['shape']
    return (inputs, input_shape)


def transform_to_grayscale(original_frame):
    if len(original_frame.shape) == 3 and original_frame.shape[2] > 1:
        return cv.cvtColor(cv.cvtColor(
            original_frame, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2RGB)
    return cv.cvtColor(original_frame, cv.COLOR_GRAY2RGB)


def transform_to_normal_lab(img_rgb):
    return cv.cvtColor(img_rgb.astype(np.float32) / 255, cv.COLOR_RGB2Lab)


def colorize_image(file, model_name):
    original_frame = convert_to_opencv(file)
    (h_orig, w_orig) = original_frame.shape[:2]

    # connect to the remote AI/ML model
    address=os.getenv("GRPC_ADDRESS", '127.0.0.1')
    port=os.getenv("GRPC_PORT", '9001')
    ovms_client = make_grpc_client("{}:{}".format(address, port))
    model_metadata = ovms_client.get_model_metadata(model_name)
    (inputs, input_shape) = prep_model_input(model_metadata)

    # transform image to grayscale LAB and input size
    h_in, w_in = input_shape[2:4]
    gray_frame = transform_to_grayscale(original_frame)
    img_lab = transform_to_normal_lab(gray_frame)
    img_l_rs = cv.resize(img_lab.copy(), (w_in, h_in))[:, :, 0]

    # send input image to model
    inputs['data_l'] = make_tensor_proto(img_l_rs, shape=input_shape)
    result = ovms_client.predict(inputs, model_name)
    update_res = np.squeeze(result)
    result = update_res.transpose((1, 2, 0))

    # resize predicted color pixels to original image
    out = cv.resize(result, (w_orig, h_orig))
    # combine original Light info with predicted colors info
    img_lab_out = np.concatenate(
        (img_lab[:, :, 0][:, :, np.newaxis], out), axis=2)
    # back to RGB and 255-scale
    img_bgr_out = np.clip(cv.cvtColor(
        img_lab_out, cv.COLOR_Lab2BGR), 0, 1) * 255

    return convert_to_bytes(img_bgr_out)
