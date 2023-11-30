import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

gdp_macro_economy = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="Table A"
)
# Load the data from the excel file
df = pd.read_excel("data/CleanedCPI.xlsx", sheet_name="Urban")

data = df[['Month', 'GENERAL INDEX (CPI)']]

# Convert the `Date` column to datetime type
data['Date'] = pd.to_datetime(data['Month'])

# Extract the year from the `Date` column
data['Year'] = data['Date'].dt.year

# Calculate the average GENERAL INDEX (CPI) for each year
yearly_cpi = data.groupby('Year')['GENERAL INDEX (CPI)'].mean().reset_index()

# Filter data from yearly_cpi DataFrame for the years 2009 to 2022
yearly_cpi_filtered = yearly_cpi[(
    yearly_cpi['Year'] >= 2009) & (yearly_cpi['Year'] <= 2022)]

yearly_cpi_filtered['Inflation Rate'] = yearly_cpi_filtered['GENERAL INDEX (CPI)'].pct_change(
)

gdp_filtered = gdp_macro_economy[(gdp_macro_economy['Year'] >= 2010) & (
    gdp_macro_economy['Year'] <= 2022)]
gdp_filtered['GDP per head (in current US dollars)'] = gdp_filtered['GDP per head (in current US dollars)'].pct_change()

merged_data = pd.merge(yearly_cpi_filtered[['Year', 'GENERAL INDEX (CPI)', 'Inflation Rate']],
                       gdp_filtered[['Year', 'Growth rate.1',
                                     'GDP per head (in current US dollars)']],
                       on='Year')

inflation_rate = 'Inflation Rate'


def display_realgdp_to_inflation():
    """Plot Real GDP to Inflation Rate using Plotly for interactivity"""

    # Create Plotly figure
    fig = go.Figure()

    # Add Inflation Rate line
    fig.add_trace(go.Scatter(
        x=merged_data['Year'],
        y=merged_data['Inflation Rate'],
        mode='lines+markers',
        name='Inflation Rate',
        line=dict(color='red')
    ))

    # Add Real GDP Growth Rate line
    fig.add_trace(go.Scatter(
        x=merged_data['Year'],
        y=merged_data['Growth rate.1'],
        mode='lines+markers',
        name='Real GDP Growth rate',
        line=dict(color='blue')
    ))

    # Update layout
    fig.update_layout(
        title='Trend of Inflation Rate and Real GDP Growth Rate over the Years',
        xaxis_title='Year',
        yaxis_title='Rate Percentage(%)',
        legend_title='Indicators',
        hovermode='x',
        height=700
    )

    fig.update_yaxes(range=[-0.05, 0.2])
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
        Inflation Rate and Real GDP Growth Rate have been fluctuating over the years showing significant economic pressures in 2020 and 2022
    </div>
    """, unsafe_allow_html=True)


def display_per_capita():
    """Plot Growth Trend of GDP per Capita over the Years with Plotly for interactivity"""

    # Create Plotly figure
    fig = go.Figure()

    # Add GDP per Capita line
    fig.add_trace(go.Scatter(
        x=merged_data['Year'],
        y=merged_data['GDP per head (in current US dollars)'],
        mode='lines+markers',
        name='Per Capita GDP',
        line=dict(color='green')
    ))

    # Update layout
    fig.update_layout(
        title='GDP per Capita Growth (In Current US Dollars)',
        xaxis_title='Year',
        yaxis_title='GDP per Capita (in current US dollars)',
        legend_title='Indicator',
        hovermode='x',
        height=535
    )

    # Adjust y-axis scale if needed
    # Example: setting range from 0 to 15000
    fig.update_yaxes(range=[-0.05, 0.2])

    # Display the figure in Streamlit
    st.plotly_chart(fig)
    st.markdown("""
    <style>
    .info {
        color: #ffff;
        background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        The Per capita Income has increased sharply following the COVID-19 pandemic year
    </div>
    """, unsafe_allow_html=True)
