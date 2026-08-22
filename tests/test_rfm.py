import pytest
import pandas as pd
import os

# Dynamic absolute paths
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")
RFM_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")

@pytest.fixture(scope="module")
def cleaned_data():
    df = pd.read_csv(CSV_PATH)
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])
    return df

@pytest.fixture(scope="module")
def rfm_data():
    return pd.read_csv(RFM_PATH)

def test_rfm_global_bounds(rfm_data):
    """Verifies that RFM values are strictly within logical bounds."""
    assert (rfm_data['Recency'] < 0).sum() == 0, "Found negative recency days."
    assert (rfm_data['Frequency'] < 1).sum() == 0, "Found frequency < 1."
    assert (rfm_data['Monetary'] <= 0).sum() == 0, "Found monetary <= 0."
    
def test_rfm_score_ranges(rfm_data):
    """Verifies that all R, F, M scores fall exactly between 1 and 5."""
    assert rfm_data['R_Score'].between(1, 5).all(), "R score out of bounds."
    assert rfm_data['F_Score'].between(1, 5).all(), "F score out of bounds."
    assert rfm_data['M_Score'].between(1, 5).all(), "M score out of bounds."

def test_manual_rfm_verification(cleaned_data, rfm_data):
    """
    Randomly selects 10 customers, manually calculates their RFM metrics 
    directly from the cleaned transaction logs, and ensures they perfectly match 
    the SQLite CTE output.
    """
    # Sample 10 customers deterministically for the test
    sample_customers = cleaned_data['customerid'].drop_duplicates().sample(n=10, random_state=42).tolist()
    
    # Calculate the snapshot date exactly as SQL does: Max(invoicedate) + 1 day
    snapshot_date = cleaned_data['invoicedate'].max() + pd.Timedelta(days=1)
    
    for customer_id in sample_customers:
        # Get customer transactions
        cust_tx = cleaned_data[cleaned_data['customerid'] == customer_id]
        
        # 1. Independent Recency
        max_date = cust_tx['invoicedate'].max()
        
        # Manual python logic to exactly mirror SQLite CAST(JULIANDAY() AS INTEGER)
        recency_delta = snapshot_date - max_date
        manual_recency = int(recency_delta.total_seconds() / 86400)
        
        # 2. Independent Frequency
        manual_frequency = cust_tx['invoiceno'].nunique()
        
        # 3. Independent Monetary (rounded to 2 decimal places as in SQL)
        manual_monetary = round(cust_tx['totalamount'].sum(), 2)
        
        # Get SQL Results
        sql_result = rfm_data[rfm_data['CustomerID'] == customer_id].iloc[0]
        
        # Assertions
        assert manual_recency == sql_result['Recency'], f"Recency mismatch for Customer {customer_id}: Manual {manual_recency} vs SQL {sql_result['Recency']}"
        assert manual_frequency == sql_result['Frequency'], f"Frequency mismatch for Customer {customer_id}: Manual {manual_frequency} vs SQL {sql_result['Frequency']}"
        
        # Floating point arithmetic comparison (allow a tiny epsilon difference)
        diff = abs(manual_monetary - sql_result['Monetary'])
        assert diff < 0.01, f"Monetary mismatch for Customer {customer_id}: Manual {manual_monetary} vs SQL {sql_result['Monetary']}"
