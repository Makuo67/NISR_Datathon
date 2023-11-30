import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
import mplcursors


gdp_growth_rate = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="Table A"
)


def display_exchange_rate_trend():
    """Plot the exchange rate trend over years
    """

    # Create Plotly figure
    fig = go.Figure()

    # Add Inflation Rate line
    fig.add_trace(go.Scatter(
        x=gdp_growth_rate['Year'],
        y=gdp_growth_rate['Exchange rate: Rwf per US dollar'],
        mode='lines+markers',
        name='Exchange Rate',
        line=dict(color='red')
    ))

    # Update layout
    fig.update_layout(
        title='Exchange Rate Trend Over Years',
        xaxis=dict(
            title='Year',
            tickmode='linear',
            dtick=1,
            tickangle=90
        ),
        yaxis=dict(title='Exchange Rate'),
        plot_bgcolor='white',
        width=780,
        height=515
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <style>
    .info {
        color: #ffff;
        background-color: #0047AB;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        GDP Growth has not really translated into a stable exchange rate.
    </div>
    """, unsafe_allow_html=True)
