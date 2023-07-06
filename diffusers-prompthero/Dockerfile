FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ARG SERVING_PORT=8000
ENV SERVING_PORT=$SERVING_PORT

WORKDIR /

RUN apt update && \
    apt install -y python3-pip

# Upgrade pip and install the copied in requirements.
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the files necessary to fetch, run and serve the model.
ADD model.py .
COPY server.py .

# Fetch the model and cache it locally.
RUN python3 model.py --fetch

# Expose the serving port.
EXPOSE $SERVING_PORT

# Run the server to handle inference requests.
CMD python3 -u server.py
