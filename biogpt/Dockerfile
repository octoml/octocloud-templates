FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ARG SERVING_PORT=8000
ENV SERVING_PORT=$SERVING_PORT

WORKDIR /
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git

# Install Python
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip
# Upgrade pip and install the copied in requirements.
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Then your code...
RUN git clone https://github.com/pytorch/fairseq && \
    cd fairseq && \
    git checkout v0.12.0 && \
    pip install . && \
    python setup.py build_ext --inplace

RUN git clone https://github.com/moses-smt/mosesdecoder.git
RUN export MOSES=${PWD}/mosesdecoder

# Clone and setup fastBPE
RUN git clone https://github.com/glample/fastBPE.git
WORKDIR /fastBPE
RUN g++ -std=c++11 -pthread -O3 -c fastBPE/main.cc -I. && g++ -std=c++11 -pthread -O3 -o fast main.o
WORKDIR /
ENV FASTBPE /fastBPE


# Copy in the files necessary to fetch, run and serve the model.
ADD model.py .
ADD server.py .

# Fetch the model and cache it locally.
RUN python3 model.py --fetch

# Expose the serving port.
EXPOSE $SERVING_PORT

# Run the server to handle inference requests.
CMD python3 -u server.py
