FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

USER root

ARG SERVING_PORT=8000
ENV SERVING_PORT=$SERVING_PORT

WORKDIR /
RUN apt-get update && apt-get upgrade -y
#RUN sudo apt-get install -y nvidia-container-toolkit
RUN apt-get install -y python3 python3-dev python3-pip git
# Upgrade pip and install the copied in requirements.
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

#RUN git clone https://github.com/pytorch/fairseq
#RUN cd fairseq
#RUN git checkout v0.12.0
#RUN pip install .
#RUN python setup.py build_ext --inplace
#RUN cd ..

RUN git clone https://github.com/moses-smt/mosesdecoder.git
RUN export MOSES=${PWD}/mosesdecoder

#RUN git clone https://github.com/glample/fastBPE.git
#RUN export FASTBPE=${PWD}/fastBPE
#RUN cd fastBPE
#RUN g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
# Copy in the files necessary to fetch, run and serve the model.
ADD model.py .
ADD server.py .

# Fetch the model and cache it locally.
RUN python3 model.py --fetch

# Expose the serving port.
EXPOSE $SERVING_PORT

# Run the server to handle inference requests.
CMD python3 -u server.py