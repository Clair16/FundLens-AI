import streamlit as st
import requests

from components.header import show_header
from components.upload import upload_document
from components.risk_card import show_risk_card
from components.dashboard import show_dashboard
from components.api import (
    send_document_to_backend,
    analyze_document
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FundLens AI",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

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


# ============================================================
# HEADER
# ============================================================

show_header()


# ============================================================
# SIDEBAR
# ============================================================

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


# ============================================================
# ANALYZE DOCUMENT PAGE
# ============================================================

if page == "📄 Analyze Document":

    uploaded_file = upload_document()

    # --------------------------------------------------------
    # FILE SELECTED
    # --------------------------------------------------------

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


        # ----------------------------------------------------
        # ANALYZE BUTTON
        # ----------------------------------------------------

        if st.button(
            "🔍 Analyze Document",
            type="primary",
            use_container_width=True
        ):

            try:

                # ==================================================
                # STEP 1 — UPLOAD PDF TO FASTAPI
                # ==================================================

                with st.spinner(
                    "📤 Uploading document..."
                ):

                    upload_result = (
                        send_document_to_backend(
                            uploaded_file
                        )
                    )


                # --------------------------------------------------
                # GET DOCUMENT ID
                # --------------------------------------------------

                document_id = upload_result[
                    "document_id"
                ]


                st.success(
                    "✅ PDF uploaded successfully."
                )


                # Show document information

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Document ID",
                        document_id
                    )

                with col2:

                    st.metric(
                        "Total Pages",
                        upload_result.get(
                            "total_pages",
                            "N/A"
                        )
                    )


                # ==================================================
                # STEP 2 — RUN RAG + GEMINI ANALYSIS
                # ==================================================

                with st.spinner(
                    "🤖 Analyzing document with AI..."
                ):

                    analysis_result = (
                        analyze_document(
                            document_id
                        )
                    )


                st.success(
                    "✅ Analysis completed successfully!"
                )


                # ==================================================
                # GET ANALYSIS OBJECT
                # ==================================================

                analysis = analysis_result[
                    "analysis"
                ]


                overall_risk = analysis.get(
                    "overall_risk",
                    "Unknown"
                )


                summary = analysis.get(
                    "summary",
                    "No summary available."
                )


                findings = analysis.get(
                    "findings",
                    []
                )


                # ==================================================
                # OVERALL RISK
                # ==================================================

                st.markdown("---")

                st.subheader(
                    "⚠️ Overall Risk"
                )


                if overall_risk == "High":

                    st.error(
                        "🔴 HIGH RISK"
                    )

                elif overall_risk == "Medium":

                    st.warning(
                        "🟡 MEDIUM RISK"
                    )

                elif overall_risk == "Low":

                    st.success(
                        "🟢 LOW RISK"
                    )

                else:

                    st.info(
                        f"Risk Level: {overall_risk}"
                    )


                # ==================================================
                # DOCUMENT SUMMARY
                # ==================================================

                st.markdown("---")

                st.subheader(
                    "📄 Document Summary"
                )

                st.write(summary)


                # ==================================================
                # ANALYSIS METRICS
                # ==================================================

                risk_count = sum(
                    1
                    for finding in findings
                    if finding.get("category")
                    == "Risk"
                )


                fee_count = sum(
                    1
                    for finding in findings
                    if finding.get("category")
                    == "Fee"
                )


                restriction_count = sum(
                    1
                    for finding in findings
                    if finding.get("category")
                    == "Restriction"
                )


                clause_count = sum(
                    1
                    for finding in findings
                    if finding.get("category")
                    == "Important Clause"
                )


                st.markdown("---")

                st.subheader(
                    "📊 Analysis Overview"
                )


                col1, col2, col3, col4 = (
                    st.columns(4)
                )


                with col1:

                    st.metric(
                        "⚠️ Risks",
                        risk_count
                    )


                with col2:

                    st.metric(
                        "💰 Fees",
                        fee_count
                    )


                with col3:

                    st.metric(
                        "🔒 Restrictions",
                        restriction_count
                    )


                with col4:

                    st.metric(
                        "📌 Clauses",
                        clause_count
                    )


                # ==================================================
                # FINDINGS
                # ==================================================

                st.markdown("---")

                st.subheader(
                    "⚠️ Risk & Important Findings"
                )


                if not findings:

                    st.info(
                        "No important findings were "
                        "identified from the document context."
                    )

                else:

                    for finding in findings:

                        show_risk_card(
                            title=finding.get(
                                "title",
                                "Untitled Finding"
                            ),

                            severity=finding.get(
                                "severity",
                                "Unknown"
                            ),

                            explanation=finding.get(
                                "explanation",
                                "No explanation available."
                            ),

                            page=finding.get(
                                "page_number",
                                "N/A"
                            )
                        )


                # ==================================================
                # PAGE LEVEL EVIDENCE
                # ==================================================

                st.markdown("---")

                st.subheader(
                    "📑 Page-Level Evidence"
                )


                if not findings:

                    st.info(
                        "No evidence available."
                    )

                else:

                    for finding in findings:

                        page_number = finding.get(
                            "page_number",
                            "N/A"
                        )

                        title = finding.get(
                            "title",
                            "Untitled Finding"
                        )

                        evidence = finding.get(
                            "evidence",
                            "No evidence available."
                        )

                        category = finding.get(
                            "category",
                            "Unknown"
                        )

                        with st.expander(
                            f"📄 Page {page_number} — {title}"
                        ):

                            st.write(
                                "**Evidence:**"
                            )

                            st.info(
                                evidence
                            )

                            st.caption(
                                f"Category: {category}"
                            )


                # ==================================================
                # READ BEFORE YOU INVEST
                # ==================================================

                st.markdown("---")

                st.subheader(
                    "📑 Read Before You Invest"
                )


                if findings:

                    for finding in findings:

                        title = finding.get(
                            "title",
                            "Important Finding"
                        )

                        explanation = finding.get(
                            "explanation",
                            ""
                        )

                        severity = finding.get(
                            "severity",
                            "Unknown"
                        )

                        page_number = finding.get(
                            "page_number",
                            "N/A"
                        )

                        st.write(
                            f"• **{title}** "
                            f"({severity}) — "
                            f"{explanation} "
                            f"*(Page {page_number})*"
                        )

                else:

                    st.write(
                        "No specific items were "
                        "identified from the retrieved "
                        "document context."
                    )


                # ==================================================
                # ANALYSIS ID
                # ==================================================

                st.markdown("---")

                st.caption(
                    f"Analysis ID: "
                    f"{analysis_result.get('analysis_id', 'N/A')}"
                )

                st.caption(
                    f"Document ID: {document_id}"
                )


            # ======================================================
            # ERROR HANDLING
            # ======================================================

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the "
                    "FastAPI backend."
                )

                st.info(
                    "Make sure FastAPI is running:"
                )

                st.code(
                    "cd backend\n"
                    "uvicorn app.main:app --reload"
                )


            except requests.exceptions.HTTPError as error:

                st.error(
                    f"❌ Backend returned an HTTP error: "
                    f"{error}"
                )


            except KeyError as error:

                st.error(
                    f"❌ Unexpected response from backend. "
                    f"Missing field: {error}"
                )

                st.json(
                    analysis_result
                    if "analysis_result" in locals()
                    else {}
                )


            except Exception as error:

                st.error(
                    f"❌ Something went wrong: {error}"
                )


# ============================================================
# DASHBOARD PAGE
# ============================================================

elif page == "📊 Dashboard":

    show_dashboard()

    st.info(
        "The dashboard will be connected to "
        "real PostgreSQL analysis data in the "
        "next step."
    )