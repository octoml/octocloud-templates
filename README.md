# octocloud-templates

This repo contains examples and templates to deploy different types of models into the OctoML Cloud.

## Prerequisites

- OctoML Cloud: [TODO: insert signup instructions here]
- Docker Hub: You have an account on [Docker Hub][dockerHub] and have authenticated the Docker CLI
  on your machine. You can learn how to authenticate your CLI [here][dockerCLIAuth].

## A simple example: Flan-T5 small

A simple example is wrapping [Google's Flan-T5 small][flant5small] model in a [Sanic][sanic] server for a simple
Q&A text2text service. You can see the server code in [model.py](./flan-t5-small/server.py).

We will start with packaging the server in a [Docker image](./flan-t5-small/Dockerfile). If you'd like to skip this
step, you can skip to Step 2 below and use our pre-packaged image at [TODO: insert image tag here].

### Step 1. Build the Docker image

Along with installing the dependencies, the Dockerfile also [downloads the model](./flan-t5-small/model.py)
into the image at build time. Because the model isn't too big, we can cache it in the Docker image for faster
startup without impacting the image size too much. If your model is larger, you may want to pull it on container
start instead of caching it in the Docker image. This may affect your container startup time, but keeps the
image itself slim.

```sh
$ DOCKER_REGISTRY="XXX" # Put your Docker Hub username here
$ cd ./flan-t5-small
$ docker build -t "$DOCKER_REGISTRY/flan-t5-small-pytorch-sanic" -f Dockerfile .
```

You can run this Docker image locally if you'd like..

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

## Step 2. Deploy into the OctoML Cloud

Now we are a few short steps to deploying our image into the OctoML Cloud. If you
skipped here and are using our pre-built image you can jump ahead. Otherwise,
push your Docker image to Docker Hub with:

```sh
$ docker push "$DOCKER_REGISTRY/flan-t5-small-pytorch-sanic"
```

Now we can deploy the image, keeping up 1 replica with the ability to autoscale up to 3 depending on
traffic load. We will deploy on an NVIDIA T4 instance, and our model will automatically
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
    -H "Authorization: Bearer $OCTOML_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"prompt":"What state is Seattle in?","max_length":100}'
$ octocloud logs --name flan-t5-small-sanic
```

Finally we can update the min replicas to 0 so it autoscales down to 0 when there is no traffic.
Note that so long as max replicas remains above 0, OctoML Cloud will autoscale your endpoint
up to max replicas to handle the traffic.

```sh
$ octocloud endpoint update --name flan-t5-small-sanic --min-replicas 0
$ octocloud endpoint list
```

TODO: Add more copy here

[dockerCLIAuth]: https://docs.docker.com/engine/reference/commandline/login/
[dockerHub]: https://hub.docker.com/
[flant5small]: https://huggingface.co/google/flan-t5-small
[sanic]: https://sanic.dev/en/
