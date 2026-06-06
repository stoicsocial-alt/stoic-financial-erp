import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def get_google_sheet(sheet_name):
    """Authenticates and returns the requested Google Sheet."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Reads credentials securely from Streamlit Cloud Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)
    return sheet

def push_to_ledger(df, sheet_name="Stoic_Social_ERP", tab_name="Transactions_Master"):
    """Appends the reconciled dataframe to the Google Sheet."""
    sheet = get_google_sheet(sheet_name)
    worksheet = sheet.worksheet(tab_name)
    
    # Convert dataframe to list of lists for gspread
    df = df.fillna("")
    data_to_upload = df.values.tolist()
    
    worksheet.append_rows(data_to_upload)
    return True
