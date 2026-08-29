import pandas as pd
import sqlite3
import os

def main():
    print("Starting data quality audit...")
    # Ensure the reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # 1. Load Data
    print("Loading data/raw/Online Retail.xlsx (this may take a moment)...")
    df = pd.read_excel("data/raw/Online Retail.xlsx")
    total_rows = len(df)
    print(f"Loaded {total_rows} rows.")
    
    # Push to SQLite for SQL checks
    print("Pushing data to in-memory SQLite database for SQL validation...")
    conn = sqlite3.connect(":memory:")
    df.to_sql("raw_sales", conn, index=False)
    
    # 2. Run SQL and Python checks
    print("Running checks...")
    
    # A. Duplicate transaction IDs
    duplicate_rows_py = df.duplicated().sum()
    dup_query = """
    SELECT SUM(cnt - 1) 
    FROM (
        SELECT InvoiceNo, StockCode, Quantity, InvoiceDate, CustomerID, COUNT(*) as cnt 
        FROM raw_sales 
        GROUP BY InvoiceNo, StockCode, Quantity, InvoiceDate, CustomerID 
        HAVING COUNT(*) > 1
    )
    """
    duplicate_rows_sql = conn.execute(dup_query).fetchone()[0] or 0
    
    # B. Negative quantities / refunds
    negative_qty_py = (df['Quantity'] < 0).sum()
    neg_qty_sql = conn.execute("SELECT COUNT(*) FROM raw_sales WHERE Quantity < 0").fetchone()[0]
    
    # C. Missing Customer IDs
    missing_customer_py = df['CustomerID'].isnull().sum()
    missing_cust_sql = conn.execute("SELECT COUNT(*) FROM raw_sales WHERE CustomerID IS NULL").fetchone()[0]
    
    # D. Inconsistent currency/units (e.g., negative or zero unit price)
    inconsistent_price_py = (df['UnitPrice'] <= 0).sum()
    inconsistent_price_sql = conn.execute("SELECT COUNT(*) FROM raw_sales WHERE UnitPrice <= 0").fetchone()[0]
    
    # 3. Output to Markdown
    print("Generating report...")
    report_content = f"""# Data Quality Audit Report

This report contains the results of the data quality audit on the raw dataset. Both SQL and Python (Pandas) methods were used to verify the integrity of the data.

**Total Rows in Raw Dataset:** {total_rows:,}

## 1. Duplicate Transaction Rows
*Rows that have identical values across Invoice, StockCode, Quantity, Date, and Customer.*
*   **Python Check (pandas.duplicated):** {duplicate_rows_py:,} rows ({duplicate_rows_py / total_rows * 100:.2f}%)
*   **SQL Check:** {duplicate_rows_sql:,} rows ({duplicate_rows_sql / total_rows * 100:.2f}%)

## 2. Negative Quantities (Refunds/Cancellations)
*Rows where the Quantity is less than zero, indicating a return or cancellation.*
*   **Python Check (Quantity < 0):** {negative_qty_py:,} rows ({negative_qty_py / total_rows * 100:.2f}%)
*   **SQL Check:** {neg_qty_sql:,} rows ({neg_qty_sql / total_rows * 100:.2f}%)

## 3. Missing Customer IDs
*Transactions that lack a Customer ID, making them impossible to track for RFM analysis.*
*   **Python Check (isnull):** {missing_customer_py:,} rows ({missing_customer_py / total_rows * 100:.2f}%)
*   **SQL Check:** {missing_cust_sql:,} rows ({missing_cust_sql / total_rows * 100:.2f}%)

## 4. Inconsistent Currency/Units (Zero or Negative Prices)
*Items that have a Unit Price of £0.00 or less, which could represent errors, bad data, or manual adjustments.*
*   **Python Check (UnitPrice <= 0):** {inconsistent_price_py:,} rows ({inconsistent_price_py / total_rows * 100:.2f}%)
*   **SQL Check:** {inconsistent_price_sql:,} rows ({inconsistent_price_sql / total_rows * 100:.2f}%)
"""
    
    with open("reports/data_quality_report.md", "w") as f:
        f.write(report_content)
    
    print("Data quality audit complete. Report written to reports/data_quality_report.md")
    
    # Enforce data quality gates
    failed = False
    if duplicate_rows_py > 0:
        print(f"\n❌ FATAL DATA QUALITY ERROR: Found {duplicate_rows_py} duplicate rows.")
        failed = True
    if inconsistent_price_py > 0:
        print(f"\n❌ FATAL DATA QUALITY ERROR: Found {inconsistent_price_py} rows with invalid prices (<= 0).")
        failed = True
        
    if failed:
        print("Pipeline aborted due to Data Quality Gate failure.")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
