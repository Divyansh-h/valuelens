import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def build_transition_matrix():
    print("Building segment transition matrix...")
    
    # Load RFM Data
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # Sort chronologically per customer
    df['Snapshot_Date'] = pd.to_datetime(df['Snapshot_Date'])
    df = df.sort_values(by=['CustomerID', 'Snapshot_Date'])
    
    # Calculate the customer's next month's segment
    df['Next_Segment'] = df.groupby('CustomerID')['Segment'].shift(-1)
    
    # Drop rows where we don't have a 'next month' to transition to (the final month of data for that customer)
    transitions = df.dropna(subset=['Next_Segment']).copy()
    
    # Compute transition probabilities
    transition_matrix = pd.crosstab(
        transitions['Segment'], 
        transitions['Next_Segment'], 
        normalize='index'
    )
    
    # Define a logical order for the axes from worst to best
    segment_order = ['Lost', 'At Risk (High Value)', 'Potential Loyalist', 'Loyal Customers', 'Champions']
    
    # Reindex to ensure consistent ordering on both axes
    transition_matrix = transition_matrix.reindex(index=segment_order, columns=segment_order, fill_value=0)
    
    # Convert to percentages for plotting readability
    transition_matrix_pct = transition_matrix * 100
    
    # Plotting
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        transition_matrix_pct, 
        annot=True, 
        fmt=".1f", 
        cmap="YlGnBu", 
        cbar_kws={'label': 'Transition Probability (%)'},
        linewidths=.5
    )
    
    plt.title('Month-Over-Month Segment Transition Matrix', pad=20, fontsize=16)
    plt.ylabel('Current Segment (Month T)', fontsize=12, labelpad=10)
    plt.xlabel('Next Segment (Month T+1)', fontsize=12, labelpad=10)
    
    plt.tight_layout()
    
    # Save output
    os.makedirs(os.path.join("reports"), exist_ok=True)
    out_path = os.path.join("reports", "transition_matrix.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    
    print(f"✅ Successfully generated and saved Transition Matrix to {out_path}")

if __name__ == "__main__":
    build_transition_matrix()
