# octocloud-templates

This repo contains examples of how to create production-grade endpoints for Machine Learnings models using the Octo Cloud.

## Prerequisites

- Octo Cloud: You can signup for an account [here](https://octoml.ai/cp/model-serving-compute-access/)
- Docker: You have an account on [Docker Hub][dockerHub], have [downloaded Docker desktop](https://www.docker.com/products/docker-desktop/) to your local machine, and have authenticated the Docker CLI
  on your machine. You can learn how to authenticate your CLI [here][dockerCLIAuth].


In this example, we will use the [Flan-T5 small](https://huggingface.co/google/flan-t5-small) model to make a production-grade endpoint for Question Answering.

## Step 1: Create a container
If you prefer using our pre-built image at [TODO: insert image tag here] rather than building one on your local machine, skip to Step 2 below.

### Prepare Python code for running an inference

First, we define how to run an inference on this model in [model.py](./flan-t5-small/model.py). The core steps include initializing the model and tokenizer using the `transformers` Python library, then running a `predict()` function that tokenizes the text input, runs the model, then de-tokenizes the model back into a text format.

### Create a server
Next, we wrap this model in a [Sanic][sanic] server in [server.py](./flan-t5-small/server.py). Sanic is a Python 3.7+ web server and web framework that’s written to go fast. In our server file, we define the following:

- A default port on which to serve inferences. The port can be any positive number, as long as it's not in use by another application. 80 is commonly used for HTTP, and 443 is often for HTTPS. In this case we choose 8000.
- Two server routes that Octo Cloud containers must have:
  - a route for inference requests (e.g. "`/predict`"). This route for inference requests must receive JSON inputs and JSON outputs.
  - a route for health checks (e.g. "`/healthcheck`")
- Number of workers (not required by Octo Cloud). Typical best practice is to make this number some function of the # of CPU cores that the server has access to and should use.


### Package the server in a Dockerfile

Now we can package the server by defining a Dockerfile(./flan-t5-small/Dockerfile). 

Along with installing the dependencies, the Dockerfile also [downloads the model](./flan-t5-small/model.py)
into the image at build time. Because the model isn't too big, we can cache it in the Docker image for faster
startup without impacting the image size too much. If your model is larger, you may want to pull it on container
start instead of caching it in the Docker image. This may affect your container startup time, but keeps the
image itself slim.


### Build a Docker image using the Dockerfile

```sh
$ DOCKER_REGISTRY="XXX" # Put your Docker Hub username here
$ cd ./flan-t5-small
$ docker build -t "$DOCKER_REGISTRY/flan-t5-small-pytorch-sanic" -f Dockerfile .
```

### Test the image locally
Run this Docker image locally to test that it can run inferences as expected:

```sh
$ docker run -d --rm \
    -p 8000:8000 --env SERVER_PORT=8000 \
    --name "flan-t5-small-pytorch-sanic"
  	"$DOCKER_REGISTRY/flan-t5-small-pytorch-sanic" 
```

..and in a separate terminal run:

```sh
$ curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    --data '{"prompt":"What state is Seattle in?","max_length":100}'
```

### Push the image to a cloud registry

Push your Docker image to Docker Hub with:
```sh
$ docker push "$DOCKER_REGISTRY/flan-t5-small-pytorch-sanic"
```

## Step 2: Run your Docker container in the Octo Cloud

Now we can create an production-grade endpoint for your Docker container, keeping up 1 replica with the ability to autoscale up to 3 depending on traffic load. We will run the endpoint on a NVIDIA T4 instance, and our model will automatically
[leverage the GPU when it's detected](./flan-t5-small/model.py).

```sh
$ DOCKER_TAG="$DOCKER_REGISTRY/flan-t5-small-pytorch-sanic" # TODO add pre-built image tag here
$ octocloud endpoint create \
    --name flan-t5-small-sanic \
    --image $DOCKER_TAG --port 8000 \
    --min-replicas 1 --max-replicas 3 \
    --instance-type t4
$ octocloud endpoint list
```

TODO: Add more instructions for UI, etc.

Once the endpoint is up, we can make requests to the automatically provisioned URL. We can
find the URL with `jq`:

```sh
$ FLAN_ENDPOINT=$(octocloud endpoint get --name flan-t5-small-sanic --output json | jq -r '.endpoint')
$ curl -X POST "$FLAN_ENDPOINT/predict" \
    -H "Authorization: Bearer $OCTOCLOUD_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"prompt":"What state is Seattle in?","max_length":100}'
$ octocloud logs --name flan-t5-small-sanic
```

Finally we can update the minimum number of replicas to 0 so that our endpoint autoscales down to 0 when there is no traffic.
Note that so long as the maximum number of replicas remains above 0, OctoML Cloud will autoscale your endpoint
up to the maximum number of replicas to handle the traffic.

```sh
$ octocloud endpoint update --name flan-t5-small-sanic --min-replicas 0
$ octocloud endpoint list
```

TODO: Add more copy here

[dockerCLIAuth]: https://docs.docker.com/engine/reference/commandline/login/
[dockerHub]: https://hub.docker.com/
[flant5small]: https://huggingface.co/google/flan-t5-small
[sanic]: https://sanic.dev/en/
