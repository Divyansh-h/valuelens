import os
import sys
from src.build_database import create_database

def main():
    try:
        print("--- ValueLens: Database Build Pipeline ---")
        db_path = os.path.join("database", "valuelens.db")
        csv_path = os.path.join("data", "processed", "cleaned_transactions.csv")
        report_path = os.path.join("reports", "database_validation.md")
        
        create_database(db_path, csv_path, report_path)
    except Exception as e:
        print(f"\n[ERROR] Database Build Pipeline Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
