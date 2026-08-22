import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ValueLens Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # Segment ordering
    segment_order = ['Champions', 'Loyal Customers', 'Potential Loyalist', 'At Risk (High Value)', 'Lost']
    df['Segment'] = pd.Categorical(df['Segment'], categories=segment_order, ordered=True)
    return df

@st.cache_data
def load_lorenz():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "lorenz_curve.csv")
    return pd.read_csv(csv_path)

try:
    df = load_data()
    lorenz_df = load_lorenz()
except FileNotFoundError:
    st.error("Data files not found. Please run the analytical pipelines first.")
    st.stop()

# --- HEADER ---
st.title("💎 ValueLens: Executive Analytics")
st.markdown("Decision Science Dashboard mapping Customer Value, Retention Risk, and Revenue Concentration.")
st.markdown("---")

# --- EXECUTIVE KPI STRIP ---
total_customers = len(df)
total_revenue = df['Monetary'].sum()
avg_value = total_revenue / total_customers

champs = df[df['Segment'] == 'Champions']
champs_pct = (len(champs) / total_customers) * 100

at_risk = df[df['Segment'] == 'At Risk (High Value)']
at_risk_rev = at_risk['Monetary'].sum()

# Top 10% Share
top_10_share = lorenz_df[lorenz_df['pct_customers'] >= 0.1].iloc[0]['pct_revenue_cumulative'] * 100

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Customers", f"{total_customers:,.0f}")
with col2:
    st.metric("Total Revenue", f"£{total_revenue/1e6:.2f}M")
with col3:
    st.metric("Avg Customer Value", f"£{avg_value:,.0f}")
with col4:
    st.metric("Champions", f"{champs_pct:.1f}%")
with col5:
    st.metric("At Risk Exposure", f"£{at_risk_rev/1e3:,.0f}k")
with col6:
    st.metric("Top 10% Reliance", f"{top_10_share:.1f}%")

st.markdown("---")

# --- ROW 1: SEGMENTATION LANDSCAPE ---
st.subheader("Segment Value Distribution")
r1c1, r1c2 = st.columns(2)

# Color Map for consistency
color_map = {
    'Champions': '#1f77b4',
    'Loyal Customers': '#2ca02c',
    'Potential Loyalist': '#ff7f0e',
    'At Risk (High Value)': '#d62728',
    'Lost': '#7f7f7f'
}

with r1c1:
    # Customer Count Donut
    segment_counts = df['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    fig1 = px.pie(segment_counts, values='Count', names='Segment', 
                  title="Customer Count Distribution", hole=0.4,
                  color='Segment', color_discrete_map=color_map)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with r1c2:
    # Revenue Bar Chart
    segment_rev = df.groupby('Segment')['Monetary'].sum().reset_index()
    fig2 = px.bar(segment_rev, x='Segment', y='Monetary', 
                  title="Total Revenue Contribution by Segment",
                  color='Segment', color_discrete_map=color_map, text_auto='.2s')
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- ROW 2: CONCENTRATION & CORRELATION ---
st.subheader("Revenue Concentration & Behavioral Correlation")
r2c1, r2c2 = st.columns(2)

with r2c1:
    # Lorenz Curve
    fig3 = px.line(lorenz_df, x='pct_customers', y='pct_revenue_cumulative',
                   title="Cumulative Revenue Concentration (Lorenz Curve)",
                   labels={'pct_customers': 'Top % of Customers', 'pct_revenue_cumulative': 'Cumulative % of Revenue'})
    
    # Add identity line
    fig3.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='gray'), name='Equality'))
    # Highlight points
    highlights = [0.01, 0.05, 0.10, 0.20]
    for h in highlights:
        idx = (lorenz_df['pct_customers'] - h).abs().idxmin()
        y_val = lorenz_df.loc[idx, 'pct_revenue_cumulative']
        fig3.add_annotation(x=h, y=y_val, text=f"Top {int(h*100)}%: {y_val*100:.1f}%", showarrow=True, arrowhead=1)
        
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    # Scatter plot
    fig4 = px.scatter(df, x='Recency', y='Monetary', color='Segment',
                      title="Recency vs. Lifetime Spend (Log Scale)",
                      color_discrete_map=color_map,
                      hover_data=['Frequency', 'CustomerID'],
                      log_y=True)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --- ROW 3: INTERVENTIONS ---
st.subheader("Strategic Interventions")
r3c1, r3c2 = st.columns([1.5, 1])

with r3c1:
    st.markdown("##### Prioritized Business Objectives")
    
    priority_data = {
        'Segment': ['At Risk (High Value)', 'Loyal Customers', 'Champions', 'Potential Loyalist', 'Lost'],
        'Priority': ['🔴 CRITICAL', '🟠 HIGH', '🟡 MED-HIGH', '🟡 MEDIUM', '⚪ LOW'],
        'Objective': ['Reactivation / Win-Back', 'Cross-Selling / AOV Lift', 'Retention / VIP Status', 'Habit Formation', 'Cost Minimization'],
        'KPI': ['Incremental Revenue', 'Avg Order Value', 'Retention Rate', '2nd Purchase %', 'Spend = £0']
    }
    st.table(pd.DataFrame(priority_data))

with r3c2:
    st.markdown("##### At Risk Reactivation Scenario")
    st.caption("Hypothetical Recovered Revenue (Not a forecast)")
    
    num_at_risk = len(at_risk)
    median_aov = (at_risk['Monetary'] / at_risk['Frequency']).median()
    
    rates = [0.05, 0.10, 0.15, 0.20]
    scenarios = []
    for r in rates:
        recovered = int(np.round(num_at_risk * r)) * median_aov
        scenarios.append({'Reactivation Rate': f"{int(r*100)}%", 'Revenue (£)': recovered})
        
    fig5 = px.bar(pd.DataFrame(scenarios), x='Reactivation Rate', y='Revenue (£)', 
                  text_auto='.3s', color_discrete_sequence=['#d62728'])
    fig5.update_layout(height=300)
    st.plotly_chart(fig5, use_container_width=True)

