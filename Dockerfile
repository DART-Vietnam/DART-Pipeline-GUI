FROM ghcr.io/kraemer-lab/dart-pipeline:v0.1.2

# add streamlit and other deps
RUN uv sync --all-extras
RUN uv tool install git+https://github.com/DART-Vietnam/dart-bias-correct

RUN apt update && \
    apt install -y --no-install-recommends \
    cdo curl

WORKDIR /
COPY gui ./gui

ENTRYPOINT [ "uv", "run", "streamlit", "run", "/gui/Main Page.py" ]