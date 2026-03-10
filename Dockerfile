# Build custom numpy for VM (no x86_64_V2)
FROM python:3.12-trixie AS builder

## Install numpy build deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y --no-install-recommends \
    gcc g++ gfortran libopenblas-dev liblapack-dev pkg-config python3-pip python3-dev git && \
    rm -rf /var/lib/apt/lists/*

## Download numpy source
WORKDIR /opt/build
RUN git clone --depth=1 https://github.com/numpy/numpy.git
WORKDIR /opt/build/numpy

## Build wheel with flags
RUN git submodule update --init
RUN python -m pip install build
RUN python -m build --wheel -Csetup-args=-Dcpu-baseline="none"

# Setup project
FROM python:3.12-slim-trixie

## Copy over numpy wheel
COPY --from=builder /opt/build/numpy/dist /dist

## Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

## Install DART-Pipeline deps
RUN apt update && apt install -y --no-install-recommends \
    cdo curl git build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

## Setup uv
RUN uv sync --all-extras
RUN uv pip install /dist/numpy-*.whl
RUN uv pip install -e .

ENTRYPOINT [ "uv", "run", "streamlit", "run", "./src/dart_pipeline_gui/Main Page.py" ]