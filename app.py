import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from calculations import calculate_laspeyres_index
from database import get_engine

# Page Config
st.set_page_config(page_title="Baku CPI Tracker", page_icon="📈", layout="wide")

st.title("Baku Alternative CPI (Consumer Price Index)")
st.markdown("Monitoring inflation in Baku supermarkets. Calculated using the **Laspeyres formula**.")

try:
    with st.spinner("Loading data from DB..."):
        engine = get_engine()
        products_df = pd.read_sql_table("products", con=engine)
        prices_df = pd.read_sql_table("price_history", con=engine)
        
        if products_df.empty or prices_df.empty:
            st.warning("⚠️ Database is empty. Please run `python main.py` in your terminal first.")
            st.stop()
            
        cpi_df = calculate_laspeyres_index(prices_df, products_df)

    # Metrics Row
    latest_cpi = cpi_df.iloc[-1]['cpi']
    prev_cpi = cpi_df.iloc[-2]['cpi'] if len(cpi_df) > 1 else 100.0
    
    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Current Index (Alt CPI)", 
        value=f"{latest_cpi:.2f} pts", 
        delta=f"{latest_cpi - prev_cpi:.2f} vs yesterday"
    )
    col2.metric(
        label="Accumulated Inflation", 
        value=f"{latest_cpi - 100.0:.2f}%",
        help="Inflation rate relative to the base period"
    )
    col3.metric(
        label="CBA Target", 
        value="4.0%", 
        delta="Target Level",
        delta_color="off"
    )

    st.divider()

    # Plotly Chart
    st.subheader("Inflation Dynamics Over Time")
    cpi_df['inflation_pct'] = cpi_df['cpi'] - 100.0
    fig = go.Figure()

    # Alt CPI Line
    fig.add_trace(go.Scatter(
        x=cpi_df['date'], 
        y=cpi_df['inflation_pct'],
        mode='lines+markers', 
        name='Alt CPI (%)',
        line=dict(color='#1f77b4', width=3)
    ))
    
    # Target Line
    fig.add_trace(go.Scatter(
        x=cpi_df['date'], 
        y=[4.0] * len(cpi_df),
        mode='lines', 
        name='CBA Target (4%)',
        line=dict(color='red', width=2, dash='dash')
    ))

    fig.update_layout(
        xaxis_title="Date", 
        yaxis_title="Inflation from Base Period (%)", 
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Raw Data Expander
    with st.expander("View Raw Data (Table)"):
        st.dataframe(cpi_df, use_container_width=True)

except Exception as e:
    st.error(f"Dashboard Error: {e}")