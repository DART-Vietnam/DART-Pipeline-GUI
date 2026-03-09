import logging

import streamlit as st

from dart_pipeline_gui.utils import prereqs_check

dart_pipeline_logger = logging.getLogger("dart_pipeline")


def run():
    prereqs_libs_df = prereqs_check()
    st.set_page_config(
        page_title="DART-Pipeline GUI",
        page_icon="⚙️",
    )

    st.title("DART-Pipeline GUI")
    st.caption("-- made with [Streamlit](https://streamlit.io/)")

    st.subheader("README")
    st.write(
        """
        Please read [the official documentation](https://dart-pipeline.readthedocs.io/en/latest/index.html)\n
        This GUI mimics the workflow outlined in the official doc above, providing a visual interface and thin wrapper around the scripts. 
        As such, there are minimal checking and validation within this GUI, please make sure you understood how DART-Pipeline works as a CLI first
        """
    )

    st.subheader("Pipeline prerequisites")
    st.write(
        "You should have all the prerequisite Python libraries and CLI executables below for DART-Pipeline to work as expected"
    )
    st.dataframe(prereqs_libs_df, hide_index=True)


if __name__ == "__main__":
    run()
