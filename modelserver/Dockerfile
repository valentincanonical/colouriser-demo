# Use the OpenVINO Toolkit development image that contains all required scripts and deps
FROM openvino/ubuntu20_dev AS omz

# Change dir for the colorization model demo
WORKDIR /opt/intel/openvino_2021.4.752/deployment_tools/open_model_zoo/demos/colorization_demo/python
# Make further commands simpler by aliasing the OMZ tools directory
ENV TOOLS /opt/intel/openvino_2021.4.752/deployment_tools/open_model_zoo/tools/downloader
RUN mkdir /home/openvino/models
# Download the latest version of the model from the Intel Open Model Zoo
RUN $TOOLS/downloader.py --list models.lst -o /home/openvino/models
# Convert the models to the OpenVINO Model Server format
RUN $TOOLS/converter.py --list models.lst -d /home/openvino/models -o /home/openvino/models --precisions FP32

# Use multi stage build to rebase our final image on the lighter OpenVINO Model Server (OMS)
FROM openvino/model_server:latest

# Copying the V1 model files 
COPY --from=omz /home/openvino/models/public/colorization-siggraph/FP32/ /models/colorize_v1/1/
# Copying the V2 model files 
COPY --from=omz /home/openvino/models/public/colorization-v2/FP32/ /models/colorize_v2/1/
# Copy the server configuration file
COPY ./models_config.json /
