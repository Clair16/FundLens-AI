import streamlit as st


def upload_document():

    st.header("Analyze a Mutual Fund Document")

    st.write(
        "Upload a mutual fund PDF to identify important "
        "risks, fees, restrictions and clauses."
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    return uploaded_file