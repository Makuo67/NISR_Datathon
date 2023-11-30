import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_excel('data/CovertGDP.xlsx', sheet_name='QGDP SH')
df2 = pd.read_excel('data/CovertGDP.xlsx', sheet_name='QGDP KP')
df.drop(columns='Unnamed: 0', axis=1, inplace=True)
df2.drop(columns='Unnamed: 0', axis=1, inplace=True)

agriculture = 'AGRICULTURE, FORESTRY & FISHING'
industry = 'INDUSTRY'
services = 'SERVICES'
taxes_and_less = 'Taxes less subsidies on products'


def display_sector_to_gdp_time_series_analysis():
    """Plot the time-series for each sector
    """

    sectors_df = df[['Quarters', 'AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY',
                    'SERVICES', 'Taxes less subsidies on products']]
    
    years = sectors_df['Quarters'].str.split().str[0].unique()
    # Create Plotly figure
    fig = go.Figure()

    # Define sector names and colors
    sectors = {
        'AGRICULTURE, FORESTRY & FISHING': 'green',
        'INDUSTRY': 'blue',
        'SERVICES': 'orange',
        'Taxes less subsidies on products': 'purple'
    }
    sectors_df['Year'] = sectors_df['Quarters'].str.split().str[0]

    # Add lines for each sector
    for sector, color in sectors.items():
        fig.add_trace(go.Scatter(
            x=sectors_df['Quarters'],
            y=sectors_df[sector],
            mode='lines',
            name=sector,
            line=dict(color=color)
        ))

    # Update layout
    fig.update_layout(
        title='GDP By Sector Time-Series Analysis at Constant Price(2017)',
        xaxis=dict(
            title='Year',
            tickmode='array',
            tickvals=[f'{year} Q1' for year in years],  # Set tick values at the first quarter of each year
            ticktext=years,  # Set tick labels to be just the year
            tickangle=90 
        ),
        yaxis_title='Percentage(%)',
        legend_title='Sectors',
        hovermode='x unified',
        width=900,
        height=500
    )

    fig.update_yaxes(range=[0, 0.52])
    # Display the figure in Streamlit
    st.plotly_chart(fig)
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
        INDUSTRY sector has increased by 33.11% since 2006Q1 to 2023Q2
    </div>
    """, unsafe_allow_html=True)

    # Calculate the change in each sector from the first to the last quarter
    sectors = ['AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY',
               'SERVICES', 'Taxes less subsidies on products']

    first_quarter = df.iloc[0][sectors]
    last_quarter = df.iloc[-1][sectors]

    change = ((last_quarter - first_quarter) / first_quarter) * 100
    change = change.sort_values(ascending=True)

    declining_sectors = change[change < 0]
    growing_sectors = change[change > 0]

    col1, col2 = st.columns((2))
    with col1:
        with st.expander("Click to see Declining Sectors", expanded=False):
            st.write(declining_sectors)
    with col2:
        with st.expander("Click to see Growing Sectors"):
            st.write(growing_sectors)


def display_quarterly_gdp():
    """Plot the GDP trend of each sector over the Quarters
    """
    # Extracting 'Quarters' and GDP columns
    data = df2[['Quarters', agriculture, industry, services, taxes_and_less]]
    gdp_columns = [agriculture, industry, services, taxes_and_less]

    # Convert the GDP columns to numeric values
    data[gdp_columns] = data[gdp_columns].apply(pd.to_numeric, errors='coerce')

    # Drop rows where any of the GDP columns have NaN values
    data = data.dropna(subset=gdp_columns)

    # Extract the year and quarter separately from the 'Quarters' column
    data['Year'] = data['Quarters'].str[:4]  # Extracting the year
    # Extracting the quarter (e.g., Q1, Q2, Q3, Q4)
    data['Quarter'] = data['Quarters'].str[-2:]

    # Aggregate the data to calculate the average GDP for each quarter across the years
    avg_quarterly_GDP = data.groupby(
        'Quarter')[gdp_columns].mean().reset_index()
    avg_quarterly_GDP['Year'] = 'Average(2006-2022)'

    # Default filter range (from 2006 to 2022)
    default_years = list(range(2006, 2023))
    default_years.insert(0, 'Average(2006-2022)')

    # Create a selectbox to filter by year within the default range
    selected_year = st.selectbox(
        'Select Year', default_years, index=0)

    # Filter data based on the selected year
    ylabel = 'Avg. Quarterly GDP (2006-2022)'
    if selected_year != 'Average(2006-2022)':
        ylabel = f"Quarterly GDP ({selected_year})"
        avg_quarterly_GDP = data[data['Year'] == str(selected_year)]

    selected_label = 'Average GDP (2006-2022)' if selected_year == 'Average(2006-2022)' else f"GDP for Year {selected_year}"

    fig = go.Figure()

    # Colors for each sector
    colors = ['green', 'blue', 'orange', 'purple']

    # Add lines for each sector
    for col, color in zip(gdp_columns, colors):
        fig.add_trace(go.Scatter(
            x=avg_quarterly_GDP['Quarter'],
            y=avg_quarterly_GDP[col],
            mode='lines+markers',
            name=col,
            line=dict(color=color)
        ))

    # Update layout
    fig.update_layout(
        title=f'Quarterly GDP Trend for {selected_label}',
        xaxis_title='Quarter',
        yaxis_title=ylabel,
        legend_title='Sectors',
        hovermode='x',
        width=900
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)
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
        Averagely, Q4 shows the highest GDP Growth for all the sectors
    </div>
    """, unsafe_allow_html=True)

# display_sector_to_gdp_time_series_analysis()
# display_quarterly_gdp()
