import sys
from src.data_ingestion import run_ingestion_pipeline

def main():
    try:
        print("--- ValueLens: Data Ingestion Pipeline ---")
        df = run_ingestion_pipeline()
        
        print("\n--- Ingestion Summary ---")
        print(f"Total Rows: {df.shape[0]:,}")
        print(f"Total Columns: {df.shape[1]}")
        print("\nSchema Information:")
        print(df.dtypes)
        print("------------------------------------------")
        
    except Exception as e:
        print(f"\n[ERROR] Ingestion Pipeline Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
