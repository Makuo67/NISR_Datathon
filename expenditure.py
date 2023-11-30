import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

gdp_expenditure_percentage = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="T3A GDP XCY"
)


def expenditure_vs_GDP(gdp_expenditure_percentage):
    # Expenditure comparison
    gdp_expenditure_percentage = gdp_expenditure_percentage[
        gdp_expenditure_percentage['Year'].between(2000, 2022)
    ]
    gdp_expenditure_percentage['GDP Growth Rate'] = gdp_expenditure_percentage['Gross Domestic Product'] * 100
    gdp_expenditure_percentage['Expenditure Growth Rate'] = gdp_expenditure_percentage['Total final consumption expenditure'] * 100

    # Create the figure
    fig = go.Figure()

    # Add GDP bar
    fig.add_trace(go.Bar(
        x=gdp_expenditure_percentage['Year'],
        y=gdp_expenditure_percentage['GDP Growth Rate'],
        name='GDP Growth Rate',
        marker=dict(color='blue')
    ))

    # Add Expenditure bar
    fig.add_trace(go.Bar(
        x=gdp_expenditure_percentage['Year'],
        y=gdp_expenditure_percentage['Expenditure Growth Rate'],
        name='Expenditure Rate',
        marker=dict(color='red')
    ))

    # Update layout for a bar chart
    fig.update_layout(
        title='GDP vs Expenditure Over Time (2017-2022)',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Growth Rate (%)', tickformat='.2f'),
        barmode='group',  # Use 'group' for grouped bar chart
        plot_bgcolor='white',
        legend_title_text='Indicator'
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)