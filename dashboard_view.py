import streamlit as st
import pandas as pd
import plotly.express as px

def render_ui(df):
    # Custom CSS for a polished, modern fintech look
    st.markdown("""
        <style>
        .stMetric {
            background-color: #f8f9fa;
            border-left: 4px solid #475569;
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .main-header {
            font-size: 2.2rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0px;
        }
        .sub-header {
            color: #64748b;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-header">Merchant MDR Copilot</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Settlement Audit & Discrepancy Tracking</p>', unsafe_allow_html=True)

    total_txn = len(df)
    total_settled = df['Settled_Amount'].sum()
    total_overcharge = df['Discrepancy_Amount'].sum()
    
    # Render metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transactions", total_txn)
    with col2:
        st.metric("Settled Volume", f"₹ {total_settled:,.2f}")
    with col3:
        st.metric("Detected Leakage", f"₹ {total_overcharge:,.2f}", delta="Audit Flag", delta_color="inverse")

    st.write("---")

    # Clean sidebar controls
    st.sidebar.header("Audit Controls")
    status_filter = st.sidebar.selectbox("Filter Status", ["All Transactions", "Discrepancy Detected", "Clean"])
    
    if status_filter != "All Transactions":
        filtered_df = df[df['Audit_Status'] == status_filter]
    else:
        filtered_df = df
        
    st.subheader("Transaction Ledger")
    
    # Soft, professional color coding (muted red/green instead of bright neon)
    def highlight_errors(val):
        if val == 'Discrepancy Detected':
            return 'background-color: #fef2f2; color: #991b1b; font-weight: 500' 
        elif val == 'Clean':
            return 'background-color: #f0fdf4; color: #166534' 
        return ''

    # hide_index=True removes the useless number column on the far left
    styled_df = filtered_df.style.map(highlight_errors, subset=['Audit_Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.write("---")
    
    st.subheader("Fee Distribution Analysis")
    
    chart_data = df.groupby('Merchant_Category')[['Actual_Fee_Deducted', 'Expected_Fee']].sum().reset_index()
    
    # Professional slate color palette for the chart
    fig = px.bar(
        chart_data, 
        x='Merchant_Category', 
        y=['Actual_Fee_Deducted', 'Expected_Fee'], 
        barmode='group',
        color_discrete_map={
            'Actual_Fee_Deducted': '#475569', 
            'Expected_Fee': '#cbd5e1'         
        },
        labels={'value': 'Amount (₹)', 'variable': 'Fee Type', 'Merchant_Category': ''}
    )
    
    # Strip out background grids for a cleaner look
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, l=0, r=0, b=0),
        legend_title_text=''
    )
    
    st.plotly_chart(fig, use_container_width=True)
