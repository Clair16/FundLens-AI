import streamlit as st
import pandas as pd

from components.api import (
    get_dashboard_stats,
    get_dashboard_findings,
    get_dashboard_documents
)


def show_dashboard():

    # ========================================================
    # HEADER
    # ========================================================

    st.header("📊 FundLens AI Dashboard")

    st.write(
        "Overview of analyzed mutual-fund documents "
        "and identified findings."
    )


    # ========================================================
    # GET DATA
    # ========================================================

    try:

        stats = get_dashboard_stats()

        findings_response = (
            get_dashboard_findings()
        )

        documents_response = (
            get_dashboard_documents()
        )

        findings = findings_response.get(
            "findings",
            []
        )

        documents = documents_response.get(
            "documents",
            []
        )


    except Exception as error:

        st.error(
            f"❌ Could not load dashboard data: {error}"
        )

        st.info(
            "Make sure FastAPI is running:"
        )

        st.code(
            "cd backend\n"
            "uvicorn app.main:app --reload"
        )

        return


    # ========================================================
    # TOP METRICS
    # ========================================================

    st.markdown("---")

    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "📄 Documents",
            stats.get(
                "documents",
                0
            )
        )


    with col2:

        st.metric(
            "⚠️ Risks",
            stats.get(
                "risks",
                0
            )
        )


    with col3:

        st.metric(
            "💰 Fees",
            stats.get(
                "fees",
                0
            )
        )


    with col4:

        st.metric(
            "🔒 Restrictions",
            stats.get(
                "restrictions",
                0
            )
        )


    # ========================================================
    # SECOND ROW
    # ========================================================

    st.markdown("---")

    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "📌 Important Clauses",
            stats.get(
                "clauses",
                0
            )
        )


    with col2:

        st.metric(
            "🔴 High",
            stats.get(
                "high",
                0
            )
        )


    with col3:

        st.metric(
            "🟡 Medium",
            stats.get(
                "medium",
                0
            )
        )


    with col4:

        st.metric(
            "🟢 Low",
            stats.get(
                "low",
                0
            )
        )


    # ========================================================
    # SEVERITY BREAKDOWN
    # ========================================================

    st.markdown("---")

    st.subheader(
        "⚠️ Severity Breakdown"
    )


    severity_data = {

        "Severity": [
            "High",
            "Medium",
            "Low"
        ],

        "Findings": [
            stats.get("high", 0),
            stats.get("medium", 0),
            stats.get("low", 0)
        ]
    }


    severity_df = pd.DataFrame(
        severity_data
    )


    st.bar_chart(
        severity_df.set_index(
            "Severity"
        )
    )


    # ========================================================
    # CATEGORY BREAKDOWN
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📊 Finding Categories"
    )


    category_data = {

        "Category": [
            "Risk",
            "Fee",
            "Restriction",
            "Important Clause"
        ],

        "Count": [
            stats.get("risks", 0),
            stats.get("fees", 0),
            stats.get("restrictions", 0),
            stats.get("clauses", 0)
        ]
    }


    category_df = pd.DataFrame(
        category_data
    )


    st.bar_chart(
        category_df.set_index(
            "Category"
        )
    )


    # ========================================================
    # RECENT FINDINGS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "⚠️ Recent Findings"
    )


    if not findings:

        st.info(
            "No findings available yet."
        )

    else:

        for finding in findings[:10]:

            severity = finding.get(
                "severity",
                "Unknown"
            )

            title = finding.get(
                "title",
                "Untitled"
            )

            category = finding.get(
                "category",
                "Unknown"
            )

            page_number = finding.get(
                "page_number",
                "N/A"
            )

            explanation = finding.get(
                "explanation",
                ""
            )


            if severity == "High":

                icon = "🔴"

            elif severity == "Medium":

                icon = "🟡"

            elif severity == "Low":

                icon = "🟢"

            else:

                icon = "⚪"


            with st.container(
                border=True
            ):

                st.write(
                    f"{icon} **{title}**"
                )

                st.caption(
                    f"{category} • "
                    f"Severity: {severity} • "
                    f"Page: {page_number}"
                )

                st.write(
                    explanation
                )


    # ========================================================
    # DOCUMENT HISTORY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📚 Analyzed Documents"
    )


    if not documents:

        st.info(
            "No documents have been analyzed yet."
        )

    else:

        document_rows = []

        for document in documents:

            document_rows.append(
                {
                    "ID":
                        document.get(
                            "id"
                        ),

                    "Filename":
                        document.get(
                            "filename"
                        ),

                    "Status":
                        document.get(
                            "status"
                        ),

                    "Created At":
                        document.get(
                            "created_at"
                        )
                }
            )


        documents_df = pd.DataFrame(
            document_rows
        )


        st.dataframe(
            documents_df,
            use_container_width=True,
            hide_index=True
        )