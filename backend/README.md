## developing

Install OpenVINO and download the Colorization-V2 model under /home/ubuntu/models/colorizationV2 with the downloader. https://docs.openvino.ai/latest/omz_demos_colorization_demo_python.html?highlight=colori
Convert the Colorization-V2 model with the converter. 
Rename `public` into `1`.

Run the OpenVINO Model Server serving the ColorizationV2 model.
```sh
docker run --rm -it -v /home/ubuntu/models/:/opt/ml:ro -p 9001:9001 -p 8001:8001 openvino/model_server:latest --model_path /opt/ml/colorizationV2 --model_name colorization-v2 --port 9001 --rest_port 8001
```

Install backend dependencies and load a python virtual env
```sh
source ./install_deps.sh
```
