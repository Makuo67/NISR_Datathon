import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

# Loading CPI data file
cpi_urban = pd.read_excel(
    io="CleanedCPI.xlsx",
    engine="openpyxl",
    sheet_name="Urban"
)

cpi_other_indices = pd.read_excel(
    io="CleanedCPI.xlsx",
    engine="openpyxl",
    sheet_name="Other_Indices"
)

def energy_vs_freshProducs_vs_general_index():
    # Create the figure
    fig = go.Figure()

    # Add a line to the figure for each index
    indices = ['General Index excluding fresh Products and energy', 'Energy index', 'Fresh Products index']
    colors = ['blue', 'red', 'green']  # Choose colors that you prefer

    for index, color in zip(indices, colors):
        fig.add_trace(go.Scatter(
            x=cpi_other_indices['Month'],
            y=cpi_other_indices[index],
            mode='lines',
            name=index,
            line=dict(color=color)
        ))

    # Update layout
    fig.update_layout(
        title='CPI-U Trends of Energy Index, Fresh Products Index and General Index',
        xaxis_title='Month',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1Y', step='year', stepmode='backward'),
                    dict(count=2, label='2Y', step='year', stepmode='backward'),
                    dict(count=3, label='3Y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            type='date',
            tickformat='%b\n%Y'  # Format the ticks to display abbreviated month and full year
        ),
        yaxis_title='CPI Index Value',
        plot_bgcolor='white',
        width=850
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)
    st.markdown("""
    <div class="info">
        The inflation in the prices of Fresh Products has increased sharply between April 2022 and September 2023, while Energy Prices and General Index Prices remain moderate
    </div>
    """, unsafe_allow_html=True)

def localGoods_vs_importedGoods():
    # CPI Trend of Local Goods vs Imported Goods
    # Create the figure
    fig = go.Figure()

    # Add a line to the figure for each index
    indices = ['Local Goods Index', 'Imported Goods Index']
    colors = ['red', 'green']  # Choose colors that you prefer

    for index, color in zip(indices, colors):
        fig.add_trace(go.Scatter(
            x=cpi_other_indices['Month'],
            y=cpi_other_indices[index],
            mode='lines',
            name=index,
            line=dict(color=color)
        ))

    # Update layout
    fig.update_layout(
        title='CPI-U Trends of Local Goods vs Imported Goods',
        xaxis_title='Month',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1Y', step='year', stepmode='backward'),
                    dict(count=2, label='2Y', step='year', stepmode='backward'),
                    dict(count=3, label='3Y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            type='date',
            tickformat='%b\n%Y'  # Format the ticks to display abbreviated month and full year
        ),
        yaxis_title='CPI Index Value',
        plot_bgcolor='white',
        width=900
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)
    st.markdown("""
    <div class="info">
        While the prices of imported goods remain higher, the trend has been moderate
    </div>
    """, unsafe_allow_html=True)
