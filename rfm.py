import sys
from src.calculate_rfm import calculate_rfm

def main():
    try:
        print("--- ValueLens: RFM Calculation Pipeline ---")
        df_rfm = calculate_rfm()
        
        print("\n--- RFM Summary ---")
        print(f"Total Customers Scored: {len(df_rfm):,}")
        
        print("\nSample High-Value Customers (Score '555'):")
        high_value = df_rfm[df_rfm['RFM_Score'] == '555']
        print(high_value.head().to_string(index=False))
        print(f"\nTotal '555' Customers: {len(high_value):,}")
        
    except Exception as e:
        print(f"\n[ERROR] RFM Calculation Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
