import streamlit as st


def show_risk_card(
    title,
    severity,
    explanation,
    page
):

    with st.container(border=True):

        st.subheader(title)

        st.write(f"Severity: {severity}")

        st.write(explanation)

        st.caption(f"📄 Source: Page {page}")