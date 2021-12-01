## How to build images

```sh
docker build . -t colorizemodelserver:latest
```

## How to run the prebuilt model server

```sh
docker run --rm -it -p 9001:9001 -p 8001:8001 colorizemodelserver:latest --config_path /models_config.json --port 9001 --rest_port 8001
```
