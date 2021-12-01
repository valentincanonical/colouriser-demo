## Start development

### Model Server
Install OpenVINO and download the models under $models_path/ with the downloader. 

Read more on [docs.openvino.ai/latest/omz_demos_colorization_demo_python.html](https://docs.openvino.ai/latest/omz_demos_colorization_demo_python.html?highlight=colori).

```sh
#!/bin/bash
python3 -m venv openvino.venv
source openvino.venv/bin/activate
python -m pip install --upgrade pip
pip install "openvino-dev[pytorch]"
export models_path=$models_path
mkdir -p $models_path
omz_downloader --name colorization-siggraph --output_dir $models_path
omz_downloader --name colorization-v2 --output_dir $models_path
```

Convert the models (Colorization-SigGraph & Colorization-V2) with the converter.

```sh
#!/bin/bash
export models_path=$models_path
export model_v1_path=$models_path/colorize_v1
export model_v2_path=$models_path/colorize_v2
# convert downloaded demo models to the OpenVINO format
omz_converter --name colorization-siggraph --precisions FP16 --download_dir $models_path --output_dir $models_path
omz_converter --name colorization-v2 --precisions FP16 --download_dir $models_path --output_dir $models_path
# create folder structure for the model serving
mkdir -p $model_v1_path $model_v2_path
mv $models_path/public/colorization-siggraph/FP16 $model_v1_path/1
mv $models_path/public/colorization-v2/FP16 $model_v2_path/1
```

Run the OpenVINO Model Server serving the ColorizationV2 model.

```sh
docker run --rm -it -v $models_path/:/models:ro -v $(pwd)/../modelserver/models_config.json:/models_config.json:ro -p 9001:9001 -p 8001:8001 openvino/model_server:latest --config_path /models_config.json --port 9001 --rest_port 8001
```

### Backend service

Install backend dependencies and load a python virtual env, then run the backend.

```sh
source ./install_deps.sh
FLASK_APP=backend.py FLASK_ENV=development flask run
```
