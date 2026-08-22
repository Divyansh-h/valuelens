import os
import pandas as pd

EXPECTED_COLUMNS = [
    "invoiceno", "stockcode", "description", "quantity", 
    "invoicedate", "unitprice", "customerid", "country"
]

def locate_raw_data(filename="Online Retail.xlsx", raw_dir="data/raw"):
    """Locate the raw dataset."""
    filepath = os.path.join(raw_dir, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")
    return filepath

def load_data(filepath):
    """Load the Excel file into a pandas DataFrame."""
    try:
        # read_excel inherently handles binary encoding for .xlsx files
        df = pd.read_excel(filepath)
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {filepath}. Error: {e}")
    return df

def normalize_columns(df):
    """Normalize column names consistently (lowercase, strip whitespace)."""
    df_norm = df.copy()
    df_norm.columns = df_norm.columns.str.strip().str.lower()
    return df_norm

def validate_schema(df):
    """Perform basic schema validation."""
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Schema validation failed. Missing expected columns: {missing_cols}")

def parse_dates(df, date_col="invoicedate"):
    """Parse the date column correctly."""
    df_parsed = df.copy()
    if date_col not in df_parsed.columns:
        raise ValueError(f"Date column '{date_col}' not found for parsing.")
    try:
        df_parsed[date_col] = pd.to_datetime(df_parsed[date_col])
    except Exception as e:
        raise ValueError(f"Failed to parse dates in column '{date_col}'. Error: {e}")
    return df_parsed

def run_ingestion_pipeline(filename="Online Retail.xlsx", raw_dir="data/raw"):
    """
    Run the full ingestion pipeline (without business cleaning).
    Returns the ingested DataFrame.
    """
    filepath = locate_raw_data(filename, raw_dir)
    print(f"Loading data from {filepath} (this may take a moment)...")
    df_raw = load_data(filepath)
    
    print("Normalizing columns...")
    df_normalized = normalize_columns(df_raw)
    
    print("Validating schema...")
    validate_schema(df_normalized)
    
    print("Parsing dates...")
    df_final = parse_dates(df_normalized)
    
    print("Data ingestion and basic validation successful.")
    return df_final
