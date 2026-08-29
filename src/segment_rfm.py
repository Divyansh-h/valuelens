import pandas as pd
import os
import sys
import yaml

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import get_logger
logger = get_logger("SegmentRFM")

def assign_segment(row, num_quintiles):
    """
    Assigns a business segment based on predefined RFM (Recency, Frequency) rules.
    Order matters due to overlapping conditions. The first matching rule wins.
    """
    if num_quintiles != 5:
        raise ValueError(f"segment_rfm rules are hardcoded for 5 quintiles. Found {num_quintiles} quintiles in config.")
        
    r = row['R_Score']
    f = row['F_Score']
    
    if r >= 4 and f >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'
    elif r <= 2 and f >= 4:
        return 'At Risk (High Value)'
    elif r <= 2 and f <= 2:
        return 'Lost'
    else:
        return 'Potential Loyalist'

        return 'Potential Loyalist'

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_segmentation():
    try:
        config = load_config()
        num_quintiles = config['rfm']['number_of_quintiles']
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        
        logger.info(f"Loading RFM data from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        logger.info(f"Applying business segmentation rules to {len(df)} rows...")
        # Apply function row by row
        df['Segment'] = df.apply(lambda row: assign_segment(row, num_quintiles), axis=1)
        
        # Reorder columns slightly for analytical convenience
        cols = ['CustomerID', 'Snapshot_Date', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score', 'Segment']
        df = df[cols]
        
        logger.info(f"Saving segmented data back to {csv_path}...")
        df.to_csv(csv_path, index=False)
        
        logger.info("--- Segmentation Summary ---")
        counts = df['Segment'].value_counts()
        for segment, count in counts.items():
            pct = (count / len(df)) * 100
            logger.info(f"{segment:<25}: {count:>5} ({pct:>5.1f}%)")
            
        logger.info("Segmentation complete.")
        
    except Exception as e:
        logger.error(f"Segmentation Pipeline Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_segmentation()
