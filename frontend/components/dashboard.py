import streamlit as st
import pandas as pd

from components.api import (
    get_dashboard_stats,
    get_dashboard_findings,
    get_dashboard_documents
)

from components import api
from components.risk_card import severity_label, show_risk_card

CATEGORIES = [
    ("Risk", "⚠️ Risks"),
    ("Fee", "💰 Fees"),
    ("Restriction", "🔒 Restrictions"),
    ("Important Clause", "📌 Clauses"),
]

<<<<<<< HEAD
DISCLAIMER = (
    "FundLens AI explains what a document says. It is not investment advice. "
    "Always verify against the original document."
)


def show_analysis_result(result: dict):
    """Render a full analysis (used by both the Analyze and Dashboard pages)."""
    findings = result.get("findings", [])

    st.subheader(f"Overall risk: {severity_label(result['overall_risk'])}")
    st.write(result["summary"])

    columns = st.columns(len(CATEGORIES))
    for column, (category, label) in zip(columns, CATEGORIES):
        column.metric(label, sum(1 for f in findings if f["category"] == category))

    st.markdown("---")

    if not findings:
        st.info("No findings were reported for this document.")
    for category, label in CATEGORIES:
        group = [f for f in findings if f["category"] == category]
        if group:
            st.subheader(label)
            for finding in sorted(group, key=lambda f: f["page_number"]):
                show_risk_card(finding)

    fees = [f for f in findings if f["category"] == "Fee"]
    if fees:
        st.subheader("💰 Fees at a glance")
        st.dataframe(
            {
                "Fee": [f["title"] for f in fees],
                "Severity": [f["severity"] for f in fees],
                "Source": [f"Page {f['page_number']}" for f in fees],
            },
            use_container_width=True,
            hide_index=True,
        )

    st.caption(DISCLAIMER)


def show_dashboard():
    st.header("📊 Dashboard")

    try:
        documents = api.list_documents()
    except Exception as error:
        st.error(f"❌ Could not load documents: {error}")
        return

    if not documents:
        st.info("No documents yet. Upload one on the Analyze Document page.")
        return

    st.dataframe(
        {
            "ID": [d["document_id"] for d in documents],
            "File": [d["filename"] for d in documents],
            "Status": [d["status"] for d in documents],
            "Overall risk": [d["overall_risk"] or "—" for d in documents],
            "Uploaded": [(d["created_at"] or "")[:16].replace("T", " ") for d in documents],
        },
        use_container_width=True,
        hide_index=True,
    )

    analyzed = [d for d in documents if d["status"] == "analyzed"]
    if not analyzed:
        return

    st.markdown("---")
    choice = st.selectbox(
        "View a saved analysis",
        analyzed,
        format_func=lambda d: f"#{d['document_id']} — {d['filename']}",
    )
    try:
        show_analysis_result(api.get_analysis(choice["document_id"]))
    except Exception as error:
        st.error(f"❌ {error}")
=======
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
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed
