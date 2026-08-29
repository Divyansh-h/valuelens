import os
import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the data cleaning rules for RFM analytics.
    
    Parameters
    ----------
    df : pd.DataFrame
        The raw ingested transaction data.
        
    Returns
    -------
    pd.DataFrame
        The cleaned, cohort-filtered, and strongly-typed transaction dataset.
        
    Raises
    ------
    AssertionError
        If the cleaning pipeline drops 100% of the rows.
    """
    df_clean = df.copy()
    
    # 1. Remove missing CustomerID
    df_clean = df_clean.dropna(subset=['customerid'])
    
    # 2. Exclude cancelled invoices (starts with C or c)
    is_cancelled = df_clean['invoiceno'].astype(str).str.startswith('C') | df_clean['invoiceno'].astype(str).str.startswith('c')
    df_clean = df_clean[~is_cancelled]
    
    # 3. Exclude Quantity <= 0
    df_clean = df_clean[df_clean['quantity'] > 0]
    
    # 4. Exclude UnitPrice <= 0
    df_clean = df_clean[df_clean['unitprice'] > 0]
    
    # 5. Remove exact duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    # 6. Remove Non-Product StockCodes (purely alphabetic)
    is_unusual = df_clean['stockcode'].astype(str).str.match('^[a-zA-Z]+$')
    df_clean = df_clean[~is_unusual]
    
    # 7. Filter for United Kingdom only to maintain cohort homogeneity
    df_clean = df_clean[df_clean['country'] == 'United Kingdom']
    
    # Ensure types
    df_clean['customerid'] = df_clean['customerid'].astype(int)
    
    # Create TotalAmount
    df_clean['totalamount'] = df_clean['quantity'] * df_clean['unitprice']
    
    # Deterministic output via sorted rows & reset index
    df_clean = df_clean.sort_values(by=['customerid', 'invoicedate', 'invoiceno', 'stockcode'])
    df_clean = df_clean.reset_index(drop=True)
    
    # 8. Data Validation Assertion
    assert len(df_clean) > 0, "FATAL ERROR: Data cleaning pipeline removed all rows."
    
    return df_clean

def generate_summary(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a before/after summary DataFrame for QA reporting.
    
    Parameters
    ----------
    df_raw : pd.DataFrame
        The raw ingested dataset.
    df_clean : pd.DataFrame
        The cleaned dataset.
        
    Returns
    -------
    pd.DataFrame
        A summary report mapping high-level changes in row counts, customers, and revenue.
    """
    raw_amount = (df_raw['quantity'] * df_raw['unitprice']).sum()
    
    summary = {
        'Metric': [
            'Row Count', 
            'Unique Customers', 
            'Unique Invoices', 
            'Total Revenue', 
            'Date Range Start', 
            'Date Range End'
        ],
        'Before Cleaning': [
            len(df_raw),
            df_raw['customerid'].nunique(dropna=True),
            df_raw['invoiceno'].nunique(),
            round(raw_amount, 2),
            df_raw['invoicedate'].min().strftime('%Y-%m-%d'),
            df_raw['invoicedate'].max().strftime('%Y-%m-%d')
        ],
        'After Cleaning': [
            len(df_clean),
            df_clean['customerid'].nunique(),
            df_clean['invoiceno'].nunique(),
            round(df_clean['totalamount'].sum(), 2),
            df_clean['invoicedate'].min().strftime('%Y-%m-%d'),
            df_clean['invoicedate'].max().strftime('%Y-%m-%d')
        ]
    }
    
    return pd.DataFrame(summary)

if __name__ == "__main__":
    print("Loading raw data...")
    raw_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "online_retail.csv")
    if not os.path.exists(raw_path):
        raw_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "Online Retail.xlsx")
        df_raw = pd.read_excel(raw_path)
    else:
        df_raw = pd.read_csv(raw_path)
        
    print("Cleaning data...")
    df_clean = clean_data(df_raw)
    
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "interim", "cleaned_sales.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df_clean.to_csv(out_path, index=False)
    print(f"Saved cleaned data to {out_path}")
