FROM ubuntu:22.04

# Set frontend to non-interactive so time zone setup does not ask questions
ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=America/Los_Angeles

ENV PYTHON_VERSION=3.10
RUN apt-get update --fix-missing && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-dev \
        python3-pip \
        python-is-python3 \
        docker.io \
        git \
        curl
RUN pip install --upgrade pip
RUN pip install --upgrade distro-info

ENV PATH="/root/.local/bin:$PATH"
WORKDIR /usr/octocloud-templates
COPY pyproject.toml poetry.lock .
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /usr/octocloud-templates

CMD ["bash"]