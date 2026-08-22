import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_scenario_analysis():
    # Paths
    csv_path = os.path.join("data", "processed", "customer_rfm.csv")
    report_path = os.path.join("reports", "scenario_analysis.md")
    fig_dir = os.path.join("reports", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    # Load Data
    df = pd.read_csv(csv_path)
    
    # Filter At Risk
    at_risk = df[df['Segment'] == 'At Risk (High Value)'].copy()
    num_customers = len(at_risk)
    
    # Calculate AOV per customer, then take the median to be extremely conservative
    at_risk['AOV'] = at_risk['Monetary'] / at_risk['Frequency']
    assumed_revenue_per_reactivation = at_risk['AOV'].median()
    
    # Scenarios
    rates = [0.05, 0.10, 0.15, 0.20]
    results = []
    
    for r in rates:
        reactivated_count = int(np.round(num_customers * r))
        recovered_revenue = reactivated_count * assumed_revenue_per_reactivation
        results.append({
            'Reactivation Rate': f"{int(r*100)}%",
            'Reactivated Customers': reactivated_count,
            'Recovered Revenue': recovered_revenue
        })
        
    results_df = pd.DataFrame(results)
    
    # Visualization
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    ax = sns.barplot(x='Reactivation Rate', y='Recovered Revenue', data=results_df, palette='Oranges_d')
    plt.title('Scenario Analysis: At Risk Reactivation Revenue (Not a Forecast)', fontsize=14, pad=15)
    plt.xlabel('Hypothetical Reactivation Rate', fontsize=12)
    plt.ylabel('Estimated Recovered Revenue (£)', fontsize=12)
    
    # Annotate
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'£{height:,.0f}', 
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='bottom', fontsize=11, xytext=(0, 5), textcoords='offset points')
                    
    plt.tight_layout()
    fig_path = os.path.join(fig_dir, '08_reactivation_scenarios.png')
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    # Markdown Report
    report_content = f"""# ValueLens: At Risk Reactivation Scenarios

> [!WARNING]
> **Scenario Analysis — Not a Forecast**
> The following table represents a hypothetical scenario analysis designed to quantify the potential financial impact of a win-back campaign. It does **not** predict or guarantee that the campaign will generate these exact conversion rates or revenue figures.

## Methodology & Assumptions

To estimate the value of reactivating an "At Risk" customer, we assume that a successful win-back campaign triggers exactly **one new transaction**. 

To estimate the value of that transaction, we use the **Median Average Order Value (AOV)** of the "At Risk" segment based on their historical data. Using the median safely guards our estimate against extreme wholesale outliers, providing a highly conservative and mathematically defensible baseline.

**The Formula:**
`Recovered Revenue = (Total "At Risk" Customers × Reactivation Rate) × Median AOV`

**The Variables:**
- Total "At Risk" Customers: **{num_customers}**
- Median AOV (At Risk Segment): **£{assumed_revenue_per_reactivation:,.2f}**

---

## Scenario Table

| Hypothetical Reactivation Rate | Reactivated Customers | Estimated Recovered Revenue |
| :--- | :--- | :--- |
| **5%** | {results_df.loc[0, 'Reactivated Customers']} | £{results_df.loc[0, 'Recovered Revenue']:,.2f} |
| **10%** | {results_df.loc[1, 'Reactivated Customers']} | £{results_df.loc[1, 'Recovered Revenue']:,.2f} |
| **15%** | {results_df.loc[2, 'Reactivated Customers']} | £{results_df.loc[2, 'Recovered Revenue']:,.2f} |
| **20%** | {results_df.loc[3, 'Reactivated Customers']} | £{results_df.loc[3, 'Recovered Revenue']:,.2f} |

*(A visual representation of this scenario analysis is saved at `reports/figures/08_reactivation_scenarios.png`)*

## Business Takeaway
Even a highly conservative **5% reactivation rate** (recovering just {results_df.loc[0, 'Reactivated Customers']} customers) yields an estimated **£{results_df.loc[0, 'Recovered Revenue']:,.0f}** in top-line revenue from a single transaction. Because these customers have proven historical buying habits, the marketing spend required to achieve a 5% conversion on this warm list is statistically far lower than attempting to acquire {results_df.loc[0, 'Reactivated Customers']} entirely new customers on the open market.
"""
    
    with open(report_path, "w") as f:
        f.write(report_content)
        
    print(f"Generated scenario analysis at {report_path}")

if __name__ == "__main__":
    run_scenario_analysis()
