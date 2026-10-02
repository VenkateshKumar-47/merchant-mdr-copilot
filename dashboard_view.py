import streamlit as st
import pandas as pd
import plotly.express as px

def render_ui(df):
    # This block injects strict CSS to remove rounded corners and smooth scroll animations
    st.markdown("""
        <style>
        * {
            border-radius: 0px !important;
        }
        html {
            scroll-behavior: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("Merchant MDR Copilot Dashboard")
    st.write("System data for expected fees and actual deductions.")

    total_txn = len(df)
    total_settled = df['Settled_Amount'].sum()
    total_overcharge = df['Discrepancy_Amount'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", total_txn)
    col2.metric("Total Settled (INR)", f"{total_settled:,.2f}")
    col3.metric("Total Overcharged (INR)", f"{total_overcharge:,.2f}", delta="Action Required", delta_color="inverse")

    st.divider()

    st.sidebar.header("Filter Data")
    st.sidebar.write("Select transaction status.")
    status_filter = st.sidebar.radio("Filter by Audit Status:", ["All", "Discrepancy Detected", "Clean"])
    
    if status_filter != "All":
        filtered_df = df[df['Audit_Status'] == status_filter]
    else:
        filtered_df = df
        
    st.subheader("Transaction Breakdown")
    
    def highlight_errors(val):
        if val == 'Discrepancy Detected':
            return 'background-color: #ffcccc; color: black'
        elif val == 'Clean':
            return 'background-color: #ccffcc; color: black'
        return ''

    styled_df = filtered_df.style.map(highlight_errors, subset=['Audit_Status'])
    st.dataframe(styled_df, use_container_width=True)

    st.divider()
    
    st.subheader("Fee Comparison by Category")
    
    chart_data = df.groupby('Merchant_Category')[['Actual_Fee_Deducted', 'Expected_Fee']].sum().reset_index()
    
    fig = px.bar(
        chart_data, 
        x='Merchant_Category', 
        y=['Actual_Fee_Deducted', 'Expected_Fee'], 
        barmode='group', 
        title="Actual Fees Deducted vs. Expected Fees (INR)",
        labels={'value': 'Amount (INR)', 'variable': 'Fee Type'}
    )
    
    st.plotly_chart(fig, use_container_width=True)