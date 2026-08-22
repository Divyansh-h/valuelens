import pytest
import sqlite3
import pandas as pd
import os

# Dynamic absolute paths based on this file's location
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "valuelens.db")
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")

@pytest.fixture(scope="module")
def cleaned_data():
    """Loads the cleaned dataset into pandas for testing."""
    df = pd.read_csv(CSV_PATH)
    # Ensure dates are parsed to check validity (pandas represents invalid dates as NaT)
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])
    return df

@pytest.fixture(scope="module")
def db_connection():
    """Provides an open SQLite database connection for testing."""
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()

# ---------------------------------------------------------
# Pandas Cleaned Dataset Tests
# ---------------------------------------------------------

def test_required_columns_exist(cleaned_data):
    """Verifies that all required columns are present in the cleaned data."""
    expected_cols = {
        'invoiceno', 'stockcode', 'description', 'quantity',
        'invoicedate', 'unitprice', 'customerid', 'country', 'totalamount'
    }
    assert expected_cols.issubset(cleaned_data.columns), "Missing required columns in cleaned data."

def test_customer_id_not_null(cleaned_data):
    """Verifies no missing CustomerIDs exist in the cleaned dataset."""
    assert cleaned_data['customerid'].isna().sum() == 0, "Found null CustomerID records."

def test_quantity_is_positive(cleaned_data):
    """Verifies that all quantities are strictly greater than zero."""
    assert (cleaned_data['quantity'] <= 0).sum() == 0, "Found zero or negative quantities."

def test_unit_price_is_positive(cleaned_data):
    """Verifies that all unit prices are strictly greater than zero."""
    assert (cleaned_data['unitprice'] <= 0).sum() == 0, "Found zero or negative unit prices."

def test_total_amount_is_positive(cleaned_data):
    """Verifies that the derived total amount is strictly greater than zero."""
    assert (cleaned_data['totalamount'] <= 0).sum() == 0, "Found zero or negative total amounts."

def test_invoice_date_is_valid(cleaned_data):
    """Verifies that InvoiceDate has no NaT (Not-a-Time) values."""
    assert cleaned_data['invoicedate'].isna().sum() == 0, "Found invalid or unparseable dates."

# ---------------------------------------------------------
# SQLite Database Tests
# ---------------------------------------------------------

def test_sales_table_exists(db_connection):
    """Verifies that the 'sales' table exists in the database."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales';")
    assert cursor.fetchone() is not None, "Table 'sales' does not exist in the database."

def test_sales_table_contains_rows(db_connection):
    """Verifies that the 'sales' table has rows inserted."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales;")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'sales' is completely empty."

def test_customer_count_is_greater_than_zero(db_connection):
    """Verifies that there are unique customers in the database."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(DISTINCT customerid) FROM sales;")
    count = cursor.fetchone()[0]
    assert count > 0, "No unique customers found in database."

def test_invoice_count_is_greater_than_zero(db_connection):
    """Verifies that there are unique invoices in the database."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(DISTINCT invoiceno) FROM sales;")
    count = cursor.fetchone()[0]
    assert count > 0, "No unique invoices found in database."

def test_revenue_is_greater_than_zero(db_connection):
    """Verifies that total revenue in the database is logically positive."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT SUM(totalamount) FROM sales;")
    revenue = cursor.fetchone()[0]
    assert revenue is not None and revenue > 0, "Total revenue is zero or negative."
