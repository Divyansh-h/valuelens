import pytest
import sqlite3
import pandas as pd
import os

@pytest.fixture(scope="module")
def sqlite_db():
    """Sets up an in-memory SQLite database with synthetic transaction data."""
    conn = sqlite3.connect(":memory:")
    
    # Create raw sales table
    conn.execute('''
        CREATE TABLE sales (
            invoiceno TEXT,
            stockcode TEXT,
            description TEXT,
            quantity INTEGER,
            invoicedate TEXT,
            unitprice REAL,
            customerid INTEGER,
            country TEXT,
            totalamount REAL
        )
    ''')
    
    # Insert synthetic data designed to test returns and longitudinal aggregation
    # Customer 101: 
    #   - Buys in Jan (+£100)
    #   - Returns in Jan (-£20)
    #   - Buys in Feb (+£50)
    data = [
        ('INV-1', 'A1', 'Product A', 10, '2011-01-05 10:00:00', 10.0, 101, 'UK', 100.0),
        ('CINV-2', 'A1', 'Product A', -2, '2011-01-15 10:00:00', 10.0, 101, 'UK', -20.0),
        ('INV-3', 'B1', 'Product B',  5, '2011-02-10 10:00:00', 10.0, 101, 'UK',  50.0),
        
        # Customer 102:
        #   - Buys in Feb (+£200)
        #   - Returns everything in March (-£200) -> Net 0
        ('INV-4', 'C1', 'Product C', 20, '2011-02-15 10:00:00', 10.0, 102, 'UK', 200.0),
        ('CINV-5', 'C1', 'Product C', -20, '2011-03-05 10:00:00', 10.0, 102, 'UK', -200.0)
    ]
    
    conn.executemany(
        "INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data
    )
    
    # Load and execute SQL files to create views
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")
    
    with open(os.path.join(sql_dir, "staging", "stg_sales.sql"), 'r') as f:
        conn.execute(f"CREATE VIEW stg_sales AS {f.read()}")
        
    with open(os.path.join(sql_dir, "intermediate", "int_monthly_snapshots.sql"), 'r') as f:
        conn.execute(f"CREATE VIEW int_monthly_snapshots AS {f.read()}")
        
    with open(os.path.join(sql_dir, "intermediate", "int_customer_rfm_monthly.sql"), 'r') as f:
        conn.execute(f"CREATE VIEW int_customer_rfm_monthly AS {f.read()}")
        
    yield conn
    conn.close()


def test_monthly_snapshot_spine(sqlite_db):
    """Verifies that the recursive CTE correctly generates end-of-month dates."""
    df = pd.read_sql("SELECT * FROM int_monthly_snapshots ORDER BY snapshot_date", sqlite_db)
    
    # Dataset range is Jan 2011 to Mar 2011
    expected_dates = ['2011-01-31', '2011-02-28', '2011-03-31']
    assert df['snapshot_date'].tolist() == expected_dates


def test_customer_101_january_aggregation(sqlite_db):
    """Verifies logic for a month containing both a purchase and a return."""
    df = pd.read_sql("SELECT * FROM int_customer_rfm_monthly WHERE customerid = 101 AND snapshot_date = '2011-01-31'", sqlite_db)
    
    assert len(df) == 1
    row = df.iloc[0]
    
    # Recency: days between 2011-01-31 and 2011-01-05 10:00 (25.58 days -> 25 truncated)
    assert row['recency_days'] == 25
    
    # Frequency: 1 valid positive purchase (INV-1). The return (CINV-2) should NOT count.
    assert row['frequency'] == 1
    
    # Monetary: £100 purchase - £20 return = £80 net
    assert row['monetary'] == 80.0


def test_customer_101_february_aggregation(sqlite_db):
    """Verifies cumulative rolling logic month-over-month."""
    df = pd.read_sql("SELECT * FROM int_customer_rfm_monthly WHERE customerid = 101 AND snapshot_date = '2011-02-28'", sqlite_db)
    
    assert len(df) == 1
    row = df.iloc[0]
    
    # Recency: days between 2011-02-28 and 2011-02-10 10:00 (17.58 days -> 17 truncated)
    assert row['recency_days'] == 17
    
    # Frequency: INV-1 in Jan + INV-3 in Feb = 2 valid purchases
    assert row['frequency'] == 2
    
    # Monetary: £80 (Jan net) + £50 (Feb purchase) = £130
    assert row['monetary'] == 130.0


def test_customer_102_negative_lifetime_value(sqlite_db):
    """Verifies handling of a customer whose lifetime value drops to zero from a full return."""
    df = pd.read_sql("SELECT * FROM int_customer_rfm_monthly WHERE customerid = 102 ORDER BY snapshot_date", sqlite_db)
    
    assert len(df) == 2 # Only spans Feb and Mar (first purchase in Feb)
    
    # Feb (before return)
    assert df.iloc[0]['monetary'] == 200.0
    
    # Mar (after return)
    assert df.iloc[1]['monetary'] == 0.0
