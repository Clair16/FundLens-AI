import streamlit as st

SEVERITY_BADGE = {"High": "🔴 High", "Medium": "🟡 Medium", "Low": "🟢 Low"}


def severity_label(severity: str) -> str:
    return SEVERITY_BADGE.get(severity, severity)


def show_risk_card(finding: dict):
    """Render one finding returned by the backend."""
    with st.container(border=True):
        st.subheader(finding["title"])
        st.write(f"**Severity:** {severity_label(finding['severity'])}  ·  "
                 f"**Type:** {finding['category']}")
        st.write(finding["explanation"])
        st.caption(f"📄 Source: Page {finding['page_number']}")
        if finding.get("evidence"):
            st.markdown(f"> {finding['evidence']}")
