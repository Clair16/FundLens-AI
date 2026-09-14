import streamlit as st


def show_dashboard():

    st.header("📊 Risk Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("⚠️ Risks", "3")

    with col2:
        st.metric("💰 Fees", "2")

    with col3:
        st.metric("🔒 Restrictions", "1")

    with col4:
        st.metric("📌 Clauses", "4")

    st.markdown("---")

    st.subheader("⚠️ Risk Findings")

    return