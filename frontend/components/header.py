import streamlit as st


def show_header():
    st.markdown(
        '<div class="main-title">📊 FundLens AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Understand mutual fund documents before you invest.'
        '</div>',
        unsafe_allow_html=True
    )