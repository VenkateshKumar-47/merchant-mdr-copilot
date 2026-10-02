import pandas as pd
import numpy as np

def run_audit(df, threshold=2000, rate=0.009, cap=50):
    """
    Applies the MDR logic to a transaction dataframe.
    threshold: Minimum amount before fees apply (default 2000)
    rate: Percentage fee applied (default 0.9%)
    cap: Maximum fee allowed per transaction (default 50)
    """
    
    audited_df = df.copy()
    
    # Calculate expected fee based on threshold limit
    # If Amount is greater than threshold, apply the rate. Otherwise, fee is 0.
    raw_fee = np.where(audited_df['Amount'] > threshold, audited_df['Amount'] * rate, 0)
    
    # Apply the maximum fee cap rule
    audited_df['Expected_Fee'] = np.minimum(raw_fee, cap)
    
    # Calculate the exact mathematical discrepancy
    audited_df['Discrepancy_Amount'] = audited_df['Actual_Fee_Deducted'] - audited_df['Expected_Fee']
    
    # Round to 2 decimal places to ensure clean currency reporting
    audited_df['Expected_Fee'] = audited_df['Expected_Fee'].round(2)
    audited_df['Discrepancy_Amount'] = audited_df['Discrepancy_Amount'].round(2)
    
    # Tag the transaction status for the dashboard to read
    # We use a 0.01 margin to ignore standard fractional rounding differences
    audited_df['Audit_Status'] = np.where(
        audited_df['Discrepancy_Amount'] > 0.01, 
        'Discrepancy Detected', 
        'Clean'
    )
    
    return audited_df