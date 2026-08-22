import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.ticker import FuncFormatter

def currency_formatter(x, pos):
    if x >= 1e6:
        return f'£{x*1e-6:.1f}M'
    elif x >= 1e3:
        return f'£{x*1e-3:.0f}K'
    else:
        return f'£{x:.0f}'

def visualize_segments():
    # File paths
    rfm_path = os.path.join("data", "processed", "customer_rfm.csv")
    summary_path = os.path.join("data", "processed", "segment_summary.csv")
    fig_dir = os.path.join("reports", "figures", "segments")
    os.makedirs(fig_dir, exist_ok=True)
    
    # Load data
    df_rfm = pd.read_csv(rfm_path)
    df_summary = pd.read_csv(summary_path)
    
    # Set aesthetics
    sns.set_theme(style="whitegrid")
    
    # Custom color palette for segments
    # Champions: Gold, Loyal: Blue, Potential: Teal, At Risk: Orange, Lost: Red
    segment_colors = {
        'Champions': '#FFD700',
        'Loyal Customers': '#4169E1',
        'Potential Loyalist': '#20B2AA',
        'At Risk (High Value)': '#FF8C00',
        'Lost': '#DC143C'
    }
    
    # Sort summary by revenue for consistent plotting
    df_summary = df_summary.sort_values('total_revenue', ascending=False)
    
    # 1. Customers by segment
    plt.figure(figsize=(10, 6))
    ax1 = sns.barplot(x='num_customers', y='Segment', data=df_summary, palette=segment_colors)
    plt.title('Number of Customers by Segment', fontsize=14, pad=15)
    plt.xlabel('Customer Count', fontsize=12)
    plt.ylabel('')
    # Annotate bars
    for i, v in enumerate(df_summary['num_customers']):
        ax1.text(v + 10, i, f"{v:,}", va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '01_customers_by_segment.png'), dpi=300)
    plt.close()
    
    # 2. Revenue by segment
    plt.figure(figsize=(10, 6))
    ax2 = sns.barplot(x='total_revenue', y='Segment', data=df_summary, palette=segment_colors)
    plt.title('Total Revenue by Segment', fontsize=14, pad=15)
    plt.xlabel('Total Revenue (£)', fontsize=12)
    plt.ylabel('')
    ax2.xaxis.set_major_formatter(FuncFormatter(currency_formatter))
    for i, v in enumerate(df_summary['total_revenue']):
        ax2.text(v + 50000, i, currency_formatter(v, None), va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '02_revenue_by_segment.png'), dpi=300)
    plt.close()
    
    # 3. Percentage of customers vs percentage of revenue
    # Prepare data for grouped bar chart
    df_melt = df_summary[['Segment', 'pct_customers', 'pct_revenue']].melt(
        id_vars='Segment', var_name='Metric', value_name='Percentage'
    )
    df_melt['Metric'] = df_melt['Metric'].map({'pct_customers': '% of Customers', 'pct_revenue': '% of Revenue'})
    
    plt.figure(figsize=(12, 6))
    ax3 = sns.barplot(x='Segment', y='Percentage', hue='Metric', data=df_melt, palette=['#87CEFA', '#32CD32'])
    plt.title('Customer Base vs. Revenue Contribution (The Pareto Effect)', fontsize=14, pad=15)
    plt.xlabel('')
    plt.ylabel('Percentage (%)', fontsize=12)
    for p in ax3.patches:
        height = p.get_height()
        if height > 0:
            ax3.annotate(f"{height:.1f}%", 
                         (p.get_x() + p.get_width() / 2., height), 
                         ha='center', va='bottom', fontsize=10, xytext=(0, 3), textcoords='offset points')
    plt.legend(title='')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '03_pct_customers_vs_revenue.png'), dpi=300)
    plt.close()
    
    # 4. Average & Median Monetary Value by Segment
    # We will plot average and median side by side to highlight the skew
    df_melt_monetary = df_summary[['Segment', 'avg_revenue', 'median_revenue']].melt(
        id_vars='Segment', var_name='Metric', value_name='Value'
    )
    df_melt_monetary['Metric'] = df_melt_monetary['Metric'].map({'avg_revenue': 'Average Spend', 'median_revenue': 'Median Spend'})
    
    plt.figure(figsize=(12, 6))
    ax4 = sns.barplot(x='Segment', y='Value', hue='Metric', data=df_melt_monetary, palette=['#9370DB', '#DDA0DD'])
    plt.title('Average vs Median Spend per Customer by Segment', fontsize=14, pad=15)
    plt.xlabel('')
    plt.ylabel('Spend (£)', fontsize=12)
    ax4.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    plt.legend(title='')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '04_avg_spend_by_segment.png'), dpi=300)
    plt.close()
    
    # 5. Recency vs Monetary scatter plot
    plt.figure(figsize=(12, 8))
    # We apply log scale to Monetary to handle extreme outliers
    ax5 = sns.scatterplot(
        x='Recency', 
        y='Monetary', 
        hue='Segment', 
        data=df_rfm, 
        palette=segment_colors,
        alpha=0.6,
        edgecolor=None,
        s=30
    )
    plt.yscale('log')
    plt.title('Recency vs Monetary Scatter Plot (Log Scale)', fontsize=14, pad=15)
    plt.xlabel('Recency (Days Since Last Purchase)', fontsize=12)
    plt.ylabel('Total Monetary Spend (£) [Log Scale]', fontsize=12)
    
    # Move legend outside the plot
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '05_recency_vs_monetary.png'), dpi=300)
    plt.close()
    
    print(f"Generated 5 segment visualizations in {fig_dir}/")

if __name__ == "__main__":
    visualize_segments()
