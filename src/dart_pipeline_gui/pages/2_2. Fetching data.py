import os
import re
from datetime import datetime
from typing import Literal, Tuple

import streamlit as st
from dart_pipeline import parse_params
from dart_pipeline.metrics import get
from dart_pipeline.paths import get_path
from streamlit.delta_generator import DeltaGenerator

from gui.utils import print_current_config


def config_has_error(fetch_start: int, fetch_end: int):
    st.subheader("Config check")

    last_supported_year = datetime.now().year
    err_flag = False

    if fetch_start > fetch_end:
        st.write("**:red[error: start year must precede end year]**")
        err_flag = True
    if fetch_end > last_supported_year:
        st.write("**:red[error: end year must not be in future]**")
        err_flag = True
    if fetch_end == last_supported_year:
        st.write("**:yellow[warn: data for the current year will be partial]**")

    return err_flag


def all_data_exist(
    region: str, fetch_start: int, fetch_end: int, type: Literal["WorldPop", "ERA5"]
) -> Tuple[bool, set[int]]:
    st.subheader(f"Check existing `{type}` data")
    path = get_path("sources", region, type.lower())

    data_files = os.listdir(path)

    if type == "WorldPop":
        regex_pat = r"vnm_p[op]p_(\d{4})_.+"
    elif type == "ERA5":
        regex_pat = r"VNM-(\d{4})-era5.grib"
    else:
        raise FileNotFoundError(f"Data files not found for `{type=}`")

    regex_compiled = re.compile(regex_pat)

    wanted_years = {year for year in range(fetch_start, fetch_end, 1)}
    exist_years = {
        int(matched.group(1))
        for file in data_files
        if (matched := regex_compiled.search(file))
    }
    missing_years = set(sorted(wanted_years - exist_years))
    no_missing_year = len(missing_years) == 0

    if no_missing_year:
        st.write(f":green[All `{type}` data in year-range already downloaded] ✅")
    else:
        st.write(f"Needs to fetch `{type}` data for years: {missing_years}")

    return (no_missing_year, missing_years)


def fetch_missing_data(
    ISO3: str,
    ADMIN: str,
    year: str,
    metric: Literal["worldpop.pop_count", "era5"],
    st_console: DeltaGenerator,
):
    parsed_subargs = parse_params([f"{ISO3}-{ADMIN}", year]).as_dict()

    get(metric, skip_process=True, **parsed_subargs)


def run():
    st.set_page_config(
        page_title="DART-Pipeline Fetching data",
        page_icon="⚙️",
    )
    st.title("DART-Pipeline Fetching data")
    st.write(
        "Fetches and prepares population and weather data for a specified ISO country code and administrative level, using the provided configuration"
    )

    #
    #############
    print_current_config(st.session_state)
    config_vars = st.session_state["config_vars"]
    fetch_start = int(config_vars["START_YEAR"].value) - 1
    fetch_end = int(config_vars["END_YEAR"].value) + 1
    ISO3 = str(config_vars["ISO3"].value)
    ADMIN = str(config_vars["ADMIN"].value)

    #
    #############
    if config_has_error(fetch_start, fetch_end):
        st.write(":red[Please resolve the errors above before continuing]")
    else:
        st.write(":green[No errors found] ✅")

    #
    #############
    pop_all_exist, pop_missing = all_data_exist(
        ISO3, fetch_start, fetch_end, "WorldPop"
    )
    era_all_exist, era_missing = all_data_exist(ISO3, fetch_start, fetch_end, "ERA5")

    #
    #############
    st.subheader("Fetch data")
    col1, col2 = st.columns([1, 1])
    with col1:
        fetch_worldpop_btn = st.button(
            "⬇️ Fetch missing WorldPop data",
            key="fetch_worldpop_btn",
            disabled=pop_all_exist,
        )
    with col2:
        fetch_era5_btn = st.button(
            "⬇️ Fetch missing ERA5 data",
            key="fetch_era5_btn",
            disabled=era_all_exist,
        )

    #
    #############
    st.session_state["log"] = ""
    st_console = st.code(st.session_state["log"], language="text", height=300)

    if fetch_worldpop_btn:
        for year in pop_missing:
            st.session_state["log"] = ""
            fetch_missing_data(ISO3, ADMIN, str(year), "worldpop.pop_count", st_console)

    if fetch_era5_btn:
        for year in era_missing:
            st.session_state["log"] = ""
            fetch_missing_data(ISO3, ADMIN, str(year), "era5", st_console)


run()
