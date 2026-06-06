import pandas as pd
import re

def process_bank_statement(uploaded_file):
    """Reads and cleans the raw bank statement."""
    df = pd.read_excel(uploaded_file, sheet_name='Account Statement')
    df = df.dropna(subset=['Transaction Date', 'Description'])
    
    # Ensure required audit columns exist
    for col in ['Entity', 'Person', 'Remarks', 'Splitwise match']:
        if col not in df.columns:
            df[col] = None
            
    return df

def apply_mapping_rules(df, rules):
    """Applies regex keywords to auto-map Entity, Person, and Remarks."""
    rules_df = pd.DataFrame(rules)
    
    for idx, row in df.iterrows():
        desc = str(row.get('Description', '')).upper()
        
        # Skip if already mapped manually in the excel
        if pd.notna(row.get('Entity')) and str(row.get('Entity')).strip() != '':
            continue

        for _, rule in rules_df.iterrows():
            if pd.notna(rule['keyword']) and re.search(rule['keyword'], desc):
                df.at[idx, 'Entity'] = rule['entity']
                df.at[idx, 'Person'] = rule['person']
                df.at[idx, 'Remarks'] = rule['remarks']
                df.at[idx, 'Splitwise match'] = rule['match']
                break # Stop searching once a rule hits
                
    return df
