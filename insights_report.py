import streamlit as st
import pandas as pd

def generate_plain_text_insights(df):
    """
    Analyzes the audited data and outputs plain-language business recommendations.
    """
    st.subheader("Audit Insights and Recommendations")
    
    discrepancy_df = df[df['Audit_Status'] == 'Discrepancy Detected']
    
    if discrepancy_df.empty:
        st.write("No discrepancies detected. Settlement matches expected deductions.")
        return

    total_loss = discrepancy_df['Discrepancy_Amount'].sum()
    error_count = len(discrepancy_df)
    
    st.write(f"System identified {error_count} flagged transactions totaling INR {total_loss:,.2f} in excess deductions.")
    
    st.write("Recommended Actions:")
    
    # Calculate which category is causing the most financial leakage
    category_losses = discrepancy_df.groupby('Merchant_Category')['Discrepancy_Amount'].sum()
    top_error_category = category_losses.idxmax()
    top_error_amount = category_losses.max()
    
    # Output plain-text bullet points
    st.write(f"* Review {top_error_category} payments: This category accounts for INR {top_error_amount:,.2f} in unexpected fees. Verify if the payment provider is applying the correct Merchant Category Code exemptions.")
    st.write("* Investigate threshold limits: Ensure transactions under the INR 2000 threshold are not being incorrectly charged.")
    st.write("* File a formal dispute: Download the reconciliation report below and submit it to your payment gateway or acquiring bank for refund processing.")

def render_export_button(df):
    """
    Creates a downloadable CSV file containing only the transactions with errors.
    """
    st.subheader("Export Reconciliation Report")
    st.write("Download the flagged transactions for bank dispute filing.")
    
    discrepancy_df = df[df['Audit_Status'] == 'Discrepancy Detected']
    
    if not discrepancy_df.empty:
        csv_data = discrepancy_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Dispute Report (CSV)",
            data=csv_data,
            file_name="mdr_discrepancy_report.csv",
            mime="text/csv"
        )
    else:
        st.write("All transactions are clean. No report required.")