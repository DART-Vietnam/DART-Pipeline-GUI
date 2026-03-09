import logging
from typing import Dict, Literal, NamedTuple

import streamlit as st
from streamlit.delta_generator import DeltaGenerator


class PreReqInfo(NamedTuple):
    Type: Literal["Python package", "CLI executable"]
    Name: str
    Status: Literal["Installed", "Missing"]
    Info: str


class ASTValueNode(NamedTuple):
    value: str
    start_byte: int
    end_byte: int


class ASTDict(Dict):
    key: str
    value: ASTValueNode


class StreamlitLogHandler(logging.Handler):
    # Initializes a custom log handler with a Streamlit container for displaying logs
    def __init__(self, container: DeltaGenerator):
        super().__init__()
        # Store the Streamlit container for log output
        self.container = container
        # Prepare an empty container for log output
        # self.log_area = self.container.empty()
        self.container.empty()
        st.session_state["log_stream"] = ""

    def emit(self, record):
        # msg = self.format(record)
        # self.log_area.markdown(record)
        st.session_state["log_stream"] += self.format(record) + "\n"
        self.container.code(st.session_state["log_stream"], language="bash", height=300)

    def clear_logs(self):
        self.container.empty()
        # self.log_area.empty()  # Clear previous logs
