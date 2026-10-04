import streamlit as st

from components import api
from components.risk_card import severity_label, show_risk_card

CATEGORIES = [
    ("Risk", "⚠️ Risks"),
    ("Fee", "💰 Fees"),
    ("Restriction", "🔒 Restrictions"),
    ("Important Clause", "📌 Clauses"),
]

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
