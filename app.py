import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE SETUP ---
st.set_page_config(
    page_title="ValueLens | Customer Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "processed", "customer_rfm.csv")
    if not os.path.exists(csv_path):
        st.error(f"Data not found at {csv_path}. Please run the pipeline first.")
        st.stop()
        
    df = pd.read_csv(csv_path)
    
    # Ensure columns exist
    if 'clv_median' not in df.columns:
        if 'predicted_clv_12m' in df.columns:
            df['clv_median'] = df['predicted_clv_12m']
        else:
            df['clv_median'] = 0.0
            
    # Load retention priority list to get rank
    priority_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "retention_priority_list.csv")
    if os.path.exists(priority_path):
        priority_df = pd.read_csv(priority_path)
        # Drop duplicates if any
        priority_df = priority_df.drop_duplicates(subset=['CustomerID'])
        priority_df = priority_df.sort_values(by='Retention_Priority_Score', ascending=False)
        priority_df['Retention_Priority_Rank'] = range(1, len(priority_df) + 1)
        
        # Merge rank and score into main df
        df = df.merge(priority_df[['CustomerID', 'Retention_Priority_Score', 'Retention_Priority_Rank']], on='CustomerID', how='left')
    else:
        df['Retention_Priority_Score'] = np.nan
        df['Retention_Priority_Rank'] = np.nan
        
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.title("🔍 ValueLens")
st.sidebar.markdown("Filter the customer database to explore specific segments.")

# Filters
segment_list = list(df['Segment'].unique())
selected_segments = st.sidebar.multiselect("RFM Segment", segment_list, default=segment_list)

cluster_list = sorted(list(df['Cluster'].unique()))
selected_clusters = st.sidebar.multiselect("K-Means Cluster", cluster_list, default=cluster_list)

min_clv, max_clv = float(df['clv_median'].min()), float(df['clv_median'].max())
clv_range = st.sidebar.slider("Predicted 12-Month CLV (£)", 
                              min_value=min_clv, 
                              max_value=max_clv, 
                              value=(min_clv, max_clv))

# Apply Filters
filtered_df = df[
    (df['Segment'].isin(selected_segments)) & 
    (df['Cluster'].isin(selected_clusters)) &
    (df['clv_median'] >= clv_range[0]) & 
    (df['clv_median'] <= clv_range[1])
]

# --- MAIN DASHBOARD ---
st.title("Customer Intelligence Dashboard")
st.markdown("Explore historically clustered behavior vs probabilistically predicted future value.")

# --- CUSTOMER LOOKUP ---
st.subheader("Individual Customer Lookup")
search_col, _ = st.columns([1, 2])
search_id = search_col.text_input("Enter Customer ID:", "")

if search_id:
    try:
        customer_id = int(search_id)
        customer_data = df[df['CustomerID'] == customer_id]
        
        if not customer_data.empty:
            cust = customer_data.iloc[0]
            st.success(f"Found Customer {customer_id}!")
            
            # Display metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("RFM Segment", cust['Segment'])
            
            rfm_string = f"R: {cust['Recency']} | F: {cust['Frequency']} | M: £{cust['Monetary']:,.0f}"
            m2.metric("RFM Behaviors", rfm_string)
            
            m3.metric("Predicted 12M CLV", f"£{cust['clv_median']:,.0f}")
            
            rank_str = f"#{int(cust['Retention_Priority_Rank'])}" if pd.notnull(cust['Retention_Priority_Rank']) else "N/A"
            m4.metric("Retention Priority Rank", rank_str)
        else:
            st.warning(f"Customer ID {customer_id} not found in the database.")
    except ValueError:
        if search_id.strip() != "":
            st.error("Please enter a valid numeric Customer ID.")

st.markdown("---")

# --- SECTION 1: KPIs ---
st.subheader("Segment Overview")
col1, col2, col3, col4 = st.columns(4)

total_customers = len(filtered_df)
total_revenue = filtered_df['Monetary'].sum()
expected_revenue = filtered_df['clv_median'].sum()
avg_clv = filtered_df['clv_median'].mean() if total_customers > 0 else 0

col1.metric("Customers in View", f"{total_customers:,}")
col2.metric("Historic Total Spend", f"£{total_revenue:,.0f}")
col3.metric("Expected Next-12M Spend", f"£{expected_revenue:,.0f}")
col4.metric("Average 12M CLV", f"£{avg_clv:,.0f}")

st.markdown("---")

# --- SECTION 2: REVENUE CONCENTRATION (PARETO) ---
st.subheader("Revenue Concentration (Pareto Analysis)")
st.markdown("This chart visualizes how heavily our future revenue relies on our top-spending 'Whales'.")

if total_customers > 0:
    # Sort by CLV descending
    pareto_df = filtered_df.sort_values(by='clv_median', ascending=False).copy()
    
    # Calculate cumulative metrics
    pareto_df['Cumulative_CLV'] = pareto_df['clv_median'].cumsum()
    pareto_df['Cumulative_Pct'] = pareto_df['Cumulative_CLV'] / expected_revenue * 100
    
    # Deciles for plotting
    pareto_df['Customer_Pct'] = np.arange(1, len(pareto_df) + 1) / len(pareto_df) * 100
    
    # For performance, if the dataset is huge, sample it for the line plot
    plot_df = pareto_df.iloc[::max(1, len(pareto_df)//100)] # 100 points
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(
        x=plot_df['Customer_Pct'],
        y=plot_df['Cumulative_Pct'],
        mode='lines',
        name='Cumulative Revenue %',
        line=dict(color='blue', width=3)
    ))
    
    # Add 80/20 reference line
    fig_pareto.add_shape(type="line", x0=20, y0=0, x1=20, y1=80, line=dict(color="red", dash="dash"))
    fig_pareto.add_shape(type="line", x0=0, y0=80, x1=20, y1=80, line=dict(color="red", dash="dash"))
    
    fig_pareto.update_layout(
        xaxis_title="% of Customer Base (Sorted by Highest Value)",
        yaxis_title="Cumulative % of Predicted 12M Revenue",
        hovermode="x unified",
        template="plotly_white"
    )
    
    st.plotly_chart(fig_pareto, use_container_width=True)
else:
    st.info("No customers match the current filter.")

st.markdown("---")

# --- SECTION 3: CLV VS RFM SCATTER PLOT ---
st.subheader("Predictive Value vs Static Behavior")
st.markdown("Hover over dots to find 'Hidden Gems' (high CLV but flagged as At-Risk) or 'False Champions' (low CLV but flagged as Champions).")

if total_customers > 0:
    # Using Recency on X-axis (log scale to spread out recent purchasers), CLV on Y axis
    # Size by Monetary, Color by Segment
    
    # Cap size for plot readability
    max_size = 50
    filtered_df['plot_size'] = np.clip(filtered_df['Monetary'] / 100, 5, max_size)
    
    # Log transform recency for better spread (adding 1 to avoid log(0))
    # We'll actually just plot Recency, but set axis to log if needed, but plotly handles it.
    
    fig_scatter = px.scatter(
        filtered_df,
        x='Recency',
        y='clv_median',
        color='Segment',
        size='plot_size',
        hover_data=['CustomerID', 'Frequency', 'Monetary', 'Cluster'],
        opacity=0.7,
        template='plotly_white',
        labels={
            'Recency': 'Days Since Last Purchase',
            'clv_median': 'Predicted 12M CLV (£)'
        }
    )
    
    # Update axes to log scale because of extreme outliers (whales)
    fig_scatter.update_layout(
        yaxis_type="log",
        xaxis_title="Recency (Days Since Last Purchase) - Lower is better",
        yaxis_title="Predicted 12-Month CLV (£) [Log Scale]",
        legend_title="RFM Segment"
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("How to read this chart"):
        st.write("""
        - **Y-Axis (CLV):** How much the probabilistic model expects the customer to spend next year.
        - **X-Axis (Recency):** How many days since their last purchase.
        - **Bubble Size:** Total historic spend.
        - **Hidden Gems:** Look for large bubbles high up on the Y-Axis, but pushed far out on the X-Axis (high recency). These are massive spenders who are at risk of churning!
        """)
