import pandas as pd
import numpy as np
import os
import sys
from lifetimes.utils import calibration_and_holdout_data
from lifetimes import BetaGeoFitter, GammaGammaFitter
from sklearn.metrics import mean_absolute_error, mean_squared_error

def validate_clv():
    try:
        print("--- ValueLens: CLV Holdout Validation ---")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")
        print(f"Loading transaction history from {csv_path}...")
        df = pd.read_csv(csv_path)
        df['invoicedate'] = pd.to_datetime(df['invoicedate']).dt.date
        
        max_date = df['invoicedate'].max()
        min_date = df['invoicedate'].min()
        print(f"Data ranges from {min_date} to {max_date}")
        
        # We will use the last 90 days as the holdout period
        calibration_end = max_date - pd.Timedelta(days=90)
        print(f"Calibration End Date: {calibration_end}")
        
        print("Splitting data into calibration and holdout periods...")
        summary_cal_holdout = calibration_and_holdout_data(
            transactions=df,
            customer_id_col='customerid',
            datetime_col='invoicedate',
            monetary_value_col='totalamount',
            calibration_period_end=calibration_end,
            observation_period_end=max_date
        )
        
        print("Filtering for customers with repeat purchases in calibration period...")
        # For Gamma-Gamma, we need frequency_cal > 0
        returning_customers = summary_cal_holdout[summary_cal_holdout['frequency_cal'] > 0].copy()
        
        print("Fitting BG/NBD Model on calibration data...")
        bgf = BetaGeoFitter(penalizer_coef=0.0)
        bgf.fit(returning_customers['frequency_cal'], returning_customers['recency_cal'], returning_customers['T_cal'])
        
        print("Fitting Gamma-Gamma Model on calibration data...")
        ggf = GammaGammaFitter(penalizer_coef=0.0)
        ggf.fit(returning_customers['frequency_cal'], returning_customers['monetary_value_cal'])
        
        print("Predicting holdout purchases and value...")
        # duration_holdout is the number of days in the holdout period for each customer
        returning_customers['predicted_purchases'] = bgf.predict(
            returning_customers['duration_holdout'],
            returning_customers['frequency_cal'],
            returning_customers['recency_cal'],
            returning_customers['T_cal']
        )
        
        returning_customers['expected_avg_profit'] = ggf.conditional_expected_average_profit(
            returning_customers['frequency_cal'],
            returning_customers['monetary_value_cal']
        )
        
        returning_customers['predicted_holdout_spend'] = returning_customers['predicted_purchases'] * returning_customers['expected_avg_profit']
        
        # Calculate actual holdout spend
        # The lifetimes package returns `monetary_value_holdout` as the average value in the holdout period, and `frequency_holdout` as the number of transactions.
        returning_customers['actual_holdout_spend'] = returning_customers['frequency_holdout'] * returning_customers['monetary_value_holdout']
        
        # Evaluation Metrics
        mae = mean_absolute_error(returning_customers['actual_holdout_spend'], returning_customers['predicted_holdout_spend'])
        rmse = np.sqrt(mean_squared_error(returning_customers['actual_holdout_spend'], returning_customers['predicted_holdout_spend']))
        
        print("\n" + "="*50)
        print("📊 CLV PREDICTION EVALUATION")
        print("="*50)
        print(f"Mean Absolute Error (MAE): £{mae:.2f}")
        print(f"Root Mean Squared Error (RMSE): £{rmse:.2f}")
        
        # Save validation results
        out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "clv_holdout_validation.csv")
        returning_customers[['predicted_holdout_spend', 'actual_holdout_spend']].to_csv(out_path)
        
        print(f"\n[Success] Validation data saved to {out_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to validate CLV: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    validate_clv()
