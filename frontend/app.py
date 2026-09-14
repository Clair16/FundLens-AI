import streamlit as st
import requests

from components.header import show_header
from components.upload import upload_document
from components.risk_card import show_risk_card
from components.dashboard import show_dashboard
from components.api import send_document_to_backend


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FundLens AI",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

show_header()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("FundLens AI")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "📄 Analyze Document",
            "📊 Dashboard"
        ]
    )

    st.markdown("---")

    st.caption(
        "FundLens AI identifies important risks, "
        "fees, restrictions and clauses from "
        "mutual-fund documents."
    )


# ==================================================
# ANALYZE DOCUMENT PAGE
# ==================================================

if page == "📄 Analyze Document":

    uploaded_file = upload_document()

    if uploaded_file:

        st.success(
            f"Document selected: {uploaded_file.name}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**File:** {uploaded_file.name}"
            )

        with col2:

            st.write(
                f"**Size:** "
                f"{uploaded_file.size / 1024:.1f} KB"
            )

        st.markdown("---")

        # ------------------------------------------
        # ANALYZE BUTTON
        # ------------------------------------------

        if st.button(
            "🔍 Analyze Document",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Uploading document to backend..."
            ):

                try:

                    # Send PDF to FastAPI
                    result = send_document_to_backend(
                        uploaded_file
                    )

                    st.success(
                        "Document uploaded successfully!"
                    )

                    # ----------------------------------
                    # BACKEND RESPONSE
                    # ----------------------------------

                    st.subheader(
                        "Backend Response"
                    )

                    st.json(result)

                    st.markdown("---")

                    # ----------------------------------
                    # TEMPORARY PHASE 1/2 PREVIEW
                    # ----------------------------------

                    st.subheader(
                        "Analysis Preview"
                    )

                    st.warning(
                        "🟡 MEDIUM — "
                        "Real document analysis will be "
                        "connected during the RAG phase."
                    )

                    st.markdown("---")

                    # ----------------------------------
                    # SUMMARY METRICS
                    # ----------------------------------

                    st.subheader(
                        "Document Summary"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "⚠️ Risks",
                            "3"
                        )

                    with col2:

                        st.metric(
                            "💰 Fees",
                            "2"
                        )

                    with col3:

                        st.metric(
                            "🔒 Restrictions",
                            "1"
                        )

                    with col4:

                        st.metric(
                            "📌 Clauses",
                            "4"
                        )

                    st.markdown("---")

                    # ----------------------------------
                    # RISK FINDINGS
                    # ----------------------------------

                    st.subheader(
                        "⚠️ Risk Findings"
                    )

                    show_risk_card(
                        title="Market Risk",
                        severity="🔴 High",
                        explanation=(
                            "The fund's returns may be "
                            "affected by fluctuations "
                            "in the market."
                        ),
                        page=17
                    )

                    show_risk_card(
                        title="Exit Load",
                        severity="🟡 Medium",
                        explanation=(
                            "An exit load may apply "
                            "when units are redeemed "
                            "within the specified period."
                        ),
                        page=23
                    )

                    show_risk_card(
                        title="Liquidity Restriction",
                        severity="🟡 Medium",
                        explanation=(
                            "Certain conditions may "
                            "restrict when investments "
                            "can be withdrawn."
                        ),
                        page=42
                    )

                    st.markdown("---")

                    # ----------------------------------
                    # FEES
                    # ----------------------------------

                    st.subheader(
                        "💰 Fees & Charges"
                    )

                    st.dataframe(
                        {
                            "Fee": [
                                "Exit Load",
                                "Expense Ratio"
                            ],
                            "Severity": [
                                "Medium",
                                "Low"
                            ],
                            "Source": [
                                "Page 23",
                                "Page 31"
                            ]
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown("---")

                    # ----------------------------------
                    # PAGE EVIDENCE
                    # ----------------------------------

                    st.subheader(
                        "📌 Page-Level Evidence"
                    )

                    st.info(
                        "Real page-level evidence will "
                        "be generated from the PDF during "
                        "the RAG integration phase."
                    )

                    st.markdown("---")

                    # ----------------------------------
                    # READ BEFORE YOU INVEST
                    # ----------------------------------

                    st.subheader(
                        "📑 Read Before You Invest"
                    )

                    st.write(
                        """
                        • Review the market-related risks
                          carefully.

                        • Check applicable exit-load
                          conditions.

                        • Understand the fees associated
                          with the fund.

                        • Review withdrawal and liquidity
                          restrictions.

                        • Verify important information
                          against the original document.
                        """
                    )

                # --------------------------------------
                # CONNECTION ERROR
                # --------------------------------------

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to the "
                        "FastAPI backend."
                    )

                    st.info(
                        "Make sure FastAPI is running with:"
                    )

                    st.code(
                        "uvicorn app.main:app --reload"
                    )

                # --------------------------------------
                # HTTP ERROR
                # --------------------------------------

                except requests.exceptions.HTTPError as error:

                    st.error(
                        f"❌ Backend returned an error: "
                        f"{error}"
                    )

                # --------------------------------------
                # OTHER ERRORS
                # --------------------------------------

                except Exception as error:

                    st.error(
                        f"❌ Something went wrong: "
                        f"{error}"
                    )


# ==================================================
# DASHBOARD PAGE
# ==================================================

elif page == "📊 Dashboard":

    show_dashboard()

    st.info(
        "Real analysis results will appear here "
        "after connecting the database and RAG pipeline."
    )