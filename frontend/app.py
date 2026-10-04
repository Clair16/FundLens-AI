import requests
import streamlit as st

from components import api
from components.dashboard import show_analysis_result, show_dashboard
from components.header import show_header
from components.upload import upload_document

st.set_page_config(page_title="FundLens AI", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
    .main-title { font-size: 42px; font-weight: 700; margin-bottom: 0px; }
    .subtitle   { font-size: 18px; color: #666; margin-bottom: 30px; }
    </style>
    """,
    unsafe_allow_html=True,
)

show_header()

with st.sidebar:
    st.header("FundLens AI")
    st.markdown("---")
    page = st.radio("Navigation", ["📄 Analyze Document", "📊 Dashboard"])
    st.markdown("---")
    st.caption(
        "FundLens AI identifies important risks, fees, restrictions and clauses "
        "from mutual-fund documents."
    )

if page == "📄 Analyze Document":
    uploaded_file = upload_document()

    if uploaded_file:
        col1, col2 = st.columns(2)
        col1.write(f"**File:** {uploaded_file.name}")
        col2.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
        st.markdown("---")

        if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
            try:
                with st.spinner("Uploading and reading the PDF..."):
                    uploaded = api.upload_pdf(uploaded_file)
                with st.spinner(f"Analyzing {uploaded['total_pages']} pages. This can take a minute..."):
                    st.session_state["result"] = api.analyze(uploaded["document_id"])
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the FastAPI backend.")
                st.code("cd backend\nuvicorn app.main:app --reload")
            except Exception as error:
                st.error(f"❌ {error}")

    if "result" in st.session_state:
        st.markdown("---")
        show_analysis_result(st.session_state["result"])

else:
    show_dashboard()
