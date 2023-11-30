import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

# Load GDP yearly data files
gdp_macro_economy = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="Table A"
)

def gdp_rate():
    # Filter data to the last six years up to 2022
    gdp_growth_data = gdp_macro_economy[gdp_macro_economy['Year']>= (2022-22)]

    # Create a Plotly figure
    fig = go.Figure()

    # Add the area chart
    fig.add_trace(go.Scatter(
    x=gdp_growth_data['Year'],
    y=gdp_growth_data['Growth rate'] * 100,
    fill='tozeroy', 
    mode='lines+markers+text',
    line_color='blue', 
    text=[f'{rate * 100:.2f}%' for rate in gdp_growth_data['Growth rate']],
    textposition='top center', 
    hoverinfo='x+y', 
    name='GDP Growth Rate'
    ))

    # Update layout
    fig.update_layout(
        title='GDP Growth Rate (2000 - 2022)',
        xaxis_title='Year',
        yaxis_title='Growth Rate (%)',
        plot_bgcolor='white'
    )

  
    st.plotly_chart(fig)
