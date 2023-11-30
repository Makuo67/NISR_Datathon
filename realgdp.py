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

sector_gdp = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="CYGDP KP"
)


def real_gdp_growth():
    last_six_years = gdp_macro_economy[gdp_macro_economy['Year'] >= (2022-22)]
    sector_data_last_six_years = sector_gdp[sector_gdp['Year'].isin(
        last_six_years['Year'])]
    # Calculate the total GDP for each year for hover information
    sector_data_last_six_years['Total GDP'] = sector_data_last_six_years[[
        'AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY', 'SERVICES', 'TAXES LESS SUBSIDIES ON PRODUCTS']].sum(axis=1)

    fig = go.Figure()
    # Add stacked bar chart for each sector

    sectors = ['AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY',
               'SERVICES', 'TAXES LESS SUBSIDIES ON PRODUCTS']
    colors = ['green', 'blue', 'red', 'orange']  # Adjust the colors as needed

    for sector, color in zip(sectors, colors):
        # Calculate the percentage for hover as a string
        sector_percentage = (
            (sector_data_last_six_years[sector] / sector_data_last_six_years['Total GDP']) * 100).astype(str)

    # Create hovertemplate string with percentage included
        hovertemplate = ['%{y:.2f} billion RWF<br>' + sector +
                         '<br>' + perc + '%' for perc in sector_percentage]

        fig.add_trace(go.Bar(
            x=sector_data_last_six_years['Year'],
            y=sector_data_last_six_years[sector],
            name=sector,
            marker_color=color,
            hovertemplate=hovertemplate
        ))

    # Update the layout for a stacked bar chart
    fig.update_layout(
        barmode='stack',
        title='Real GDP Growth (2000 - 2022)',
        yaxis=dict(
            tickmode='auto',
            tickformat=',.1f',  # This will format the tick as a floating number with two decimal places
            title='GDP (in billion RWF)'
        ),
        xaxis=dict(tickmode='array',
                   tickvals=sector_data_last_six_years['Year']),
        plot_bgcolor='white',
        width=750
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
        The Real GDP has been growing consistently with a notable expansion in the services sectors, suggesting increasing sectors economic growth.
    </div>
    """, unsafe_allow_html=True)
