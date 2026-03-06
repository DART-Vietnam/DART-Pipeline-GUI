import os

import streamlit as st

from gui.utils import print_current_config, run_subproc


def run():
    st.set_page_config(
        page_title="DART-Pipeline Processing data",
        page_icon="⚙️",
    )
    st.title("DART-Pipeline Processing data")
    st.markdown(
        """
        Processes weather data for a configured region and time range. This includes:
         - Fitting gamma parameters for SPI and SPEI
         - Running SPI and SPEI calculations
         - Processing core weather variables at weekly or daily resolution
         - Optionally applying bias correction
         - Concatenating output when using weekly resolution
        """
    )

    #
    #############
    print_current_config(st.session_state)
    config_vars = st.session_state["config_vars"]
    TEMPORAL_RESOLUTION = config_vars["TEMPORAL_RESOLUTION"].value
    BC_ENABLE = config_vars["BC_ENABLE"].value
    ISO3 = config_vars["ISO3"].value
    ADMIN = config_vars["ADMIN"].value
    START_YEAR = config_vars["START_YEAR"].value
    END_YEAR = config_vars["END_YEAR"].value

    #
    #############
    if TEMPORAL_RESOLUTION not in ["weekly", "daily"]:
        st.write(
            ":red[Error: invalid TEMPORAL_RESOLUTION, must be one of 'daily' or 'weekly']"
        )

    #
    #############
    cmd_list = [
        "uv",
        "run",
        "dart-pipeline",
        "process",
        "era5",
        f"{ISO3}-{ADMIN}",
        f"{START_YEAR}-{END_YEAR}",
        f"temporal_resolution='{TEMPORAL_RESOLUTION}'",
        "overwrite",
    ]
    if BC_ENABLE != 1:
        cmd_list.append("skip_correction")

    #
    #############
    st.subheader("Process data")
    proc_dat = st.button("Click to process data", key="proc_dat_btn")

    st.session_state["log"] = ""
    st_console = st.code(st.session_state["log"], language="bash", height=300)

    if proc_dat:
        st.session_state["log"] = ""
        subproc = run_subproc(
            cmd_list,
            st_console,
            st.session_state,
        )

        if subproc.returncode == 0:
            st.write("Data processing finished")
        else:
            st.write(f"Data processing killed with {subproc.returncode=}")


run()
