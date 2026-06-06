import streamlit as st

st.set_page_config(page_title="B&I Financial ERP", page_icon="🏢", layout="centered")

st.title("Welcome to the B&I Financial ERP")
st.markdown("""
Use the sidebar to navigate between modules:
*   **Reconciliation:** Upload your monthly bank statements and map transactions.
*   **Dashboard:** View runway, burn rate, and entity-specific P&L.
""")
