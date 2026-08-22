import sqlite3
import pandas as pd
import os

def create_database(db_path, csv_path, report_path):
    print(f"Connecting to database at {db_path}...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Dropping existing sales table if it exists (idempotency)...")
    cursor.execute("DROP TABLE IF EXISTS sales;")
    
    print("Creating sales table schema...")
    cursor.execute("""
    CREATE TABLE sales (
        invoiceno TEXT,
        stockcode TEXT,
        description TEXT,
        quantity INTEGER,
        invoicedate DATETIME,
        unitprice REAL,
        customerid INTEGER,
        country TEXT,
        totalamount REAL
    );
    """)
    
    print("Loading cleaned dataset...")
    df = pd.read_csv(csv_path)
    # Ensure invoicedate is string format for SQLite
    df['invoicedate'] = pd.to_datetime(df['invoicedate']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    print("Inserting data into SQLite (this may take a few seconds)...")
    df.to_sql('sales', conn, if_exists='append', index=False)
    
    print("Creating indexes to optimize RFM aggregations...")
    cursor.execute("CREATE INDEX idx_customerid ON sales(customerid);")
    cursor.execute("CREATE INDEX idx_invoiceno ON sales(invoiceno);")
    cursor.execute("CREATE INDEX idx_invoicedate ON sales(invoicedate);")
    
    conn.commit()
    
    # Verification
    print("Running validation queries directly on the SQLite database...")
    
    row_count = cursor.execute("SELECT COUNT(*) FROM sales;").fetchone()[0]
    customer_count = cursor.execute("SELECT COUNT(DISTINCT customerid) FROM sales;").fetchone()[0]
    invoice_count = cursor.execute("SELECT COUNT(DISTINCT invoiceno) FROM sales;").fetchone()[0]
    min_date = cursor.execute("SELECT MIN(invoicedate) FROM sales;").fetchone()[0]
    max_date = cursor.execute("SELECT MAX(invoicedate) FROM sales;").fetchone()[0]
    total_revenue = cursor.execute("SELECT SUM(totalamount) FROM sales;").fetchone()[0]
    
    validation_md = f"""# Database Validation Report

The `valuelens.db` SQLite database has been successfully built and populated with the cleaned transaction data.

## Verification Metrics (Queried directly from SQLite)
- **Row Count**: `{row_count:,}` (Expected: 348,914)
- **Unique Customers**: `{customer_count:,}` (Expected: 3,917)
- **Unique Invoices**: `{invoice_count:,}` (Expected: 16,590)
- **Date Range Start**: `{min_date}` 
- **Date Range End**: `{max_date}` 
- **Total Revenue**: `£{total_revenue:,.2f}` (Expected: £7,244,495.32)

## Schema & Indexes
- Table: `sales`
- Indexes Created:
  - `idx_customerid`: Accelerates `GROUP BY customerid` for customer-level RFM aggregations.
  - `idx_invoiceno`: Accelerates invoice-level lookups and basket analyses.
  - `idx_invoicedate`: Accelerates time-series filtering and Recency calculations.
"""
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(validation_md)
        
    print(f"Validation report written to {report_path}")
    
    conn.close()
    print("Database build complete.")
