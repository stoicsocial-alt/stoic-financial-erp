import streamlit as st
import pandas as pd
from core.reconciliation import process_bank_statement, apply_mapping_rules
from core.constants import DEFAULT_MAPPING_RULES
from core.database import push_to_ledger

st.set_page_config(page_title="Reconciliation", layout="wide")
st.title("Bank Statement Auditor")

uploaded_file = st.file_uploader("Upload Monthly Bank Statement (.xls/.xlsx)", type=['xls', 'xlsx'])

if uploaded_file:
    # 1. Process and Map (Controller Logic)
    with st.spinner("Processing document..."):
        raw_df = process_bank_statement(uploaded_file)
        mapped_df = apply_mapping_rules(raw_df, DEFAULT_MAPPING_RULES)
        
    unmapped_mask = mapped_df['Entity'].isna() | (mapped_df['Entity'] == '')
    
    # 2. Human-in-the-Loop UI (View Logic)
    st.subheader("Action Required: Unmapped Transactions")
    if unmapped_mask.any():
        unmapped_df = mapped_df[unmapped_mask].copy()
        
        edited_unmapped = st.data_editor(
            unmapped_df[['Transaction Date', 'Description', 'Withdrawals', 'Deposits', 'Entity', 'Person', 'Remarks']],
            column_config={
                "Entity": st.column_config.SelectboxColumn("Entity", options=["Socialight", "Bold and Italic", "Ignore/Personal"]),
                "Person": st.column_config.TextColumn("Person/Client"),
            },
            disabled=["Transaction Date", "Description", "Withdrawals", "Deposits"],
            use_container_width=True,
            key="manual_override"
        )
        
        # Merge edits back to master dataframe
        mapped_df.loc[unmapped_mask, ['Entity', 'Person', 'Remarks']] = edited_unmapped[['Entity', 'Person', 'Remarks']]
    else:
        st.success("All transactions were successfully mapped!")

    # 3. Database Sync (Model Logic)
    st.divider()
    if st.button("Sync to Google Sheets", type="primary"):
        try:
            with st.spinner("Pushing to ledger..."):
                push_to_ledger(mapped_df)
            st.success("Ledger updated successfully!")
            st.balloons()
        except Exception as e:
            st.error(f"Failed to sync to Database: {e}")
