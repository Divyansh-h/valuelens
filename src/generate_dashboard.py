import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_static_dashboard():
    # Setup directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dash_dir = os.path.join(base_dir, "reports", "dashboard")
    fig_dir = os.path.join(dash_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    # Load data
    df = pd.read_csv(os.path.join(base_dir, "data", "processed", "customer_rfm.csv"))
    # Calculate Lorenz Curve dynamically
    df_sorted = df.sort_values(by='Monetary', ascending=False)
    lorenz_df = pd.DataFrame({
        'pct_customers': np.arange(1, len(df_sorted) + 1) / len(df_sorted),
        'pct_revenue_cumulative': df_sorted['Monetary'].cumsum() / df_sorted['Monetary'].sum()
    })
    total_customers = len(df)
    total_revenue = df['Monetary'].sum()
    avg_value = total_revenue / total_customers
    champs = df[df['Segment'] == 'Champions']
    champs_pct = (len(champs) / total_customers) * 100
    at_risk = df[df['Segment'] == 'At Risk (High Value)']
    at_risk_rev = at_risk['Monetary'].sum()
    top_10_share = lorenz_df[lorenz_df['pct_customers'] >= 0.1].iloc[0]['pct_revenue_cumulative'] * 100
    
    # Generate new static charts directly into dashboard folder
    segment_order = ['Champions', 'Loyal Customers', 'Potential Loyalist', 'At Risk (High Value)', 'Lost']
    df['Segment'] = pd.Categorical(df['Segment'], categories=segment_order, ordered=True)
    
    # Chart 1: Segment Distribution
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, y='Segment', palette='viridis')
    plt.title("Customer Count by Segment")
    plt.xlabel("Number of Customers")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '01_segment_dist.png'), dpi=300)
    plt.close()
    
    # Chart 2: Revenue by Segment
    plt.figure(figsize=(10, 5))
    seg_rev = df.groupby('Segment')['Monetary'].sum().reset_index()
    sns.barplot(data=seg_rev, y='Segment', x='Monetary', palette='viridis')
    plt.title("Total Revenue by Segment (£)")
    plt.xlabel("Revenue (£)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '02_segment_rev.png'), dpi=300)
    plt.close()
    
    # Chart 3: RFM Scatter
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Recency', y='Monetary', hue='Segment', palette='viridis', alpha=0.6)
    plt.yscale('log')
    plt.title("Recency vs Lifetime Spend (Log Scale)")
    plt.xlabel("Recency (Days since last purchase)")
    plt.ylabel("Lifetime Spend (£)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '03_rfm_scatter.png'), dpi=300)
    plt.close()
    
    # Chart 4: Revenue Concentration (Lorenz)
    plt.figure(figsize=(8, 8))
    plt.plot(lorenz_df['pct_customers'], lorenz_df['pct_revenue_cumulative'], color='blue', lw=2)
    plt.plot([0,1], [0,1], color='gray', linestyle='--')
    plt.title("Revenue Concentration (Lorenz Curve)")
    plt.xlabel("Top % of Customers")
    plt.ylabel("Cumulative % of Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '04_revenue_concentration.png'), dpi=300)
    plt.close()
    
    # Chart 5: Scenario Analysis
    num_at_risk = len(at_risk)
    median_aov = (at_risk['Monetary'] / at_risk['Frequency']).median()
    rates = [0.05, 0.10, 0.15, 0.20]
    scenarios = []
    for r in rates:
        recovered = int(np.round(num_at_risk * r)) * median_aov
        scenarios.append({'Reactivation Rate': f"{int(r*100)}%", 'Recovered Revenue (£)': recovered})
    
    plt.figure(figsize=(8, 5))
    scen_df = pd.DataFrame(scenarios)
    ax = sns.barplot(data=scen_df, x='Reactivation Rate', y='Recovered Revenue (£)', palette='Reds_d')
    plt.title("At Risk Reactivation Scenarios (Estimated £)")
    
    for p in ax.patches:
        ax.annotate(f"£{p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '05_scenario_analysis.png'), dpi=300)
    plt.close()
    
    # Markdown Content
    md = f"""# ValueLens: Executive Analytics Dashboard

This dashboard is a lightweight, reproducible analytical report synthesized dynamically from the core ValueLens dataset.

## 1. Executive Summary (KPIs)

| Metric | Value |
| :--- | :--- |
| **Total Customers** | {total_customers:,.0f} |
| **Total Revenue** | £{total_revenue:,.2f} |
| **Avg Customer Value** | £{avg_value:,.2f} |
| **Champions %** | {champs_pct:.1f}% |
| **At Risk Revenue** | £{at_risk_rev:,.2f} |
| **Top 10% Revenue Share** | {top_10_share:.1f}% |

---

## 2. Customer Segment Overview

We map our customer base across 5 heuristic behavioral segments based on Recency and Frequency.

![Segment Distribution](figures/01_segment_dist.png)

---

## 3. Revenue Contribution

While "Lost" customers dominate the headcount, the "Champions" segment holds the vast majority of financial value.

![Revenue by Segment](figures/02_segment_rev.png)

---

## 4. Revenue Concentration

The Lorenz curve demonstrates our exposure. The top 10% of customers generate nearly {top_10_share:.0f}% of total revenue.

![Revenue Concentration](figures/04_revenue_concentration.png)

---

## 5. RFM Visualization

Visualizing the correlation between high Recency (low days) and massive Lifetime Spend (Log Scale).

![RFM Scatter](figures/03_rfm_scatter.png)

---

## 6. Retention Opportunity & Scenario Analysis

**Objective**: Rescue the "At Risk (High Value)" segment.
**Risk**: £{at_risk_rev:,.0f} in capital exposure.

The following model calculates the estimated top-line revenue recovered from a deep-discount win-back campaign, assuming it triggers a single transaction at the historical Median AOV of the segment. *(Note: This is a scenario analysis, not a guaranteed forecast).*

![Scenario Analysis](figures/05_scenario_analysis.png)
"""
    
    with open(os.path.join(dash_dir, "ValueLens_Dashboard.md"), "w") as f:
        f.write(md)
        
    print("Static Dashboard generated successfully at reports/dashboard/ValueLens_Dashboard.md")

if __name__ == "__main__":
    generate_static_dashboard()
