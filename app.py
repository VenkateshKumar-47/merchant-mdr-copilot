import streamlit as st
from data_pipeline import load_data
from audit_engine import run_audit
from dashboard_view import render_ui
from insights_report import generate_plain_text_insights, render_export_button

# Configure the main page settings
st.set_page_config(page_title="Merchant MDR Copilot", layout="wide")

def main():
    """
    Main execution sequence linking all four modules together.
    """
    # Step 1: Execute Data Pipeline
    df = load_data()
    
    if df is not None:
        # Step 2: Execute Audit Engine
        audited_df = run_audit(df)
        
        # Step 3: Render Dashboard UI
        render_ui(audited_df)
        
        # Step 4: Generate Insights and Export Tools
        generate_plain_text_insights(audited_df)
        render_export_button(audited_df)

if __name__ == "__main__":
    main()