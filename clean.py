import os
import sys
from src.data_ingestion import run_ingestion_pipeline
from src.clean_data import clean_data, generate_summary

def main():
    try:
        print("--- ValueLens: Data Cleaning Pipeline ---")
        df_raw = run_ingestion_pipeline()
        
        print("\nApplying cleaning rules...")
        df_clean = clean_data(df_raw)
        
        print("Generating summary...")
        summary_df = generate_summary(df_raw, df_clean)
        
        print("\n--- Cleaning Summary ---")
        print(summary_df.to_string(index=False))
        
        processed_path = os.path.join("data", "processed", "cleaned_transactions.csv")
        print(f"\nSaving cleaned dataset to {processed_path}...")
        df_clean.to_csv(processed_path, index=False)
        
        export_path = os.path.join("data", "exports", "cleaning_summary.csv")
        print(f"Saving cleaning summary to {export_path}...")
        summary_df.to_csv(export_path, index=False)
        
        print("Cleaning pipeline complete.")
        
    except Exception as e:
        print(f"\n[ERROR] Cleaning Pipeline Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
