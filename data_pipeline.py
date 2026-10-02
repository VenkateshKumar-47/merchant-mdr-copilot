import pandas as pd
import streamlit as st
import random
from datetime import datetime, timedelta

def generate_mock_data():
    """
    Generates 50 dummy transactions with intentional deduction errors for testing.
    """
    data = []
    start_date = datetime(2026, 10, 15)
    categories = ['Grocery', 'Electronics', 'Pharmacy', 'Apparel']
    
    for i in range(1, 51):
        txn_id = f"TXN{1000 + i}"
        date = start_date + timedelta(days=random.randint(0, 10))
        amount = round(random.uniform(500, 5000), 2)
        category = random.choice(categories)
        
        # Expected baseline logic: threshold is 2000, rate is 0.9 percent, cap is 50
        if amount > 2000:
            expected_fee = min(amount * 0.009, 50.0)
        else:
            expected_fee = 0.0
            
        actual_fee = expected_fee
        
        # Plant deliberate overcharge errors in a subset of transactions
        if i % 8 == 0:
            actual_fee = expected_fee + random.uniform(10, 30)
            
        actual_fee = round(actual_fee, 2)
        settled_amount = round(amount - actual_fee, 2)
        
        data.append([txn_id, date.strftime('%Y-%m-%d'), amount, 'UPI', category, settled_amount, actual_fee])
        
    columns = ['Transaction_ID', 'Date', 'Amount', 'Payment_Mode', 'Merchant_Category', 'Settled_Amount', 'Actual_Fee_Deducted']
    return pd.DataFrame(data, columns=columns)

def load_data():
    """
    Provides the UI for file uploads and returns a validated Pandas DataFrame.
    """
    st.write("Upload your settlement CSV file or load the sample audit data.")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = ['Amount', 'Actual_Fee_Deducted', 'Settled_Amount', 'Merchant_Category']
            
            # Schema validation
            if not all(col in df.columns for col in required_columns):
                st.error("Error: Uploaded CSV is missing required columns. Please check your file format.")
                return None
            return df
        except Exception:
            st.error("Error: Could not read the uploaded file.")
            return None
    else:
        st.write("No file uploaded. Use the sample data to test the system.")
        if st.button("Load Sample Audit Data"):
            return generate_mock_data()
        return None