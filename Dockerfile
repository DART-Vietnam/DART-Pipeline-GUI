# Setup project
FROM python:3.12-slim-trixie

## Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

## Install DART-Pipeline deps
RUN apt update && apt install -y --no-install-recommends \
    cdo curl git build-essential && \
    rm -rf /var/lib/apt/lists/*

## Copy in uv settings and deps
COPY pyproject.toml uv.lock numpy-2.4.3-cp312-cp312-linux_x86_64.whl config.sh /app/
COPY src/ /app/src
WORKDIR /app

## Setup uv
RUN uv sync --all-extras
RUN uv pip install -e .

ENTRYPOINT [ "uv", "run", "streamlit", "run", "./src/dart_pipeline_gui/Main Page.py" ]