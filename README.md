# coloriser-demo
OpenVINO on Ubuntu Containers demo running a Coloriser app with MicroK8s

## Deploy with Kubernetes

### MicroK8s
> You can skip this step if you already have a Kubernetes cluster at hand.

Setup MicroK8s to quickly get a Kubernetes cluster on your machine.

```sh
sudo snap install microk8s --classic
microk8s enable dns storage
microk8s status --wait-ready
```

### Build components images


### Deployment


## Components 

### Backend

Interface frontend <> OMS

### Model Server

Serves the Colorization Model

```sh
docker run --rm -it -p 9001:9001 colorisationv2:latest --model_path /opt/ml/ColorizationV2 --model_name colorization --port 9001
# docker run --rm -it -p 9001:9001 colorisationsig:latest --model_path /opt/ml/ColorizationSig --model_name colorization --port 9001
```

### Front end

A sweet interface to use the model!