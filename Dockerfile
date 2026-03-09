FROM python:3.13-slim-trixie

# setup uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# setup sys deps for `pyproj` and `numpy`
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y --no-install-recommends \
    cdo curl git && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN uv sync --all-extras
RUN uv pip install -e .

ENTRYPOINT [ "uv", "run", "streamlit", "run", "./src/dart_pipeline_gui/Main Page.py" ]