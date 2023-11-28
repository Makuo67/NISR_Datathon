import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
    page_title="GDP and CPI DashBoard",
    page_icon=":bar_chart:",
    layout="wide"
)

# Load GDP yearly data files
gdp_macro_economy = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="Table A"
)

gdp_expenditure = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="T3 GDP CY"
)
st.dataframe(gdp_expenditure)
sector_gdp = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="CYGDP KP"
)

gdp_expenditure_percentage = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="T3A GDP XCY"
)


# Load GDP quarterly data files
quarterly_gdp = pd.read_excel(
    io="CovertGDP.xlsx",
    engine="openpyxl",
    sheet_name="QGDP KP"
)
## Loading CPI data file
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

# Display the title with emoji centered
st.markdown(
    '<div style="text-align: center;">'
    '<h1 style="display: inline-block; margin-bottom: 0;">&#x1F4CA; Rwanda Economic Dashboard: Insights into GDP & Inflation Dynamics</h1>'
    '<div style="height: 2px; background-color: #ccc; width: 80%; margin: 0 auto;"></div>'
    '</div>',
    unsafe_allow_html=True
)

# Get the lastest GDP, CPI, Population and Inflation values from the data frames
last_gdp_value = quarterly_gdp['GROSS DOMESTIC PRODUCT (GDP)'].iloc[-1]
last_gdp_quarter = quarterly_gdp['Quarters'].iloc[-1]
last_cpi_value = cpi_urban['GENERAL INDEX (CPI)'].iloc[-1]
inflation_rate = ((cpi_urban['GENERAL INDEX (CPI)'].iloc[-1] / cpi_urban['GENERAL INDEX (CPI)'].iloc[-13]) - 1) * 100
last_population_value = gdp_macro_economy['Total population (millions)'].iloc[-1]

cards_data = [
    {
        'title': 'Gross Domestic Product',
        'subtitle': 'Constant 2017 prices, Billions RWF',
        'time': f'{last_gdp_quarter}',
        'value': f"{last_gdp_value:.2f}",
        'icon': '💼' 
    },
    {
        'title': 'Consumer Price Index',
        'subtitle': 'February 2014 = 100',
        'time': 'October 2023',
        'value': f"{last_cpi_value:.1f}",
        'icon': '🛒'
    },
    {
        'title': 'Inflation Rate',
        'subtitle': 'Year-over-Year',
        'time': 'October 2023',
        'value': f"{inflation_rate:.2f}%",  
        'icon': '📈'
    },
    {
        'title': 'Population Size',
        'subtitle': 'Number (millions)',
        'time': '2022',
        'value': f"{last_population_value:.2f}M",
        'icon': '👥'  # Replace with suitable emoji or image
    }
]

st.markdown("""
<style>
.card {
    background-color: #2258a9; /* Change the background color as needed */
    color: white; /* Text color */
    padding: 20px;
    border-radius: 10px; /* Adjust the border radius as needed */
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15); /* Optional: Adds a shadow effect */
    transition: transform 0.2s; /* Optional: Adds a slight 'pop' effect on hover */
    margin: 10px;
}
.card:hover {
    transform: scale(1.05); /* Optional: Slight zoom effect on hover */
}
.card h1 {
    color: #ffff; /* Color for the icon and value */
}
.card h4 {
    color: black; /* Black title color */
    font-weight: bold; /* Make the title bolder */
    margin-bottom: 0.5rem; /* Space below the title */
}
</style>
""", unsafe_allow_html=True)

# Loop through the data and create two columns for each row
for i in range(0, len(cards_data), 2):
    cols = st.columns(2)
    for j in range(2):
        # Check if the card exists (for the last row if the number of cards is odd)
        if i + j < len(cards_data):
            card = cards_data[i + j]
            with cols[j]:
                # Use the "card" class for styling
                st.markdown(f"""
                <div class="card">
                    <h4>{card['title']}</h4>
                    <p>{card['subtitle']}</p>
                    <p>{card['time']}</p>
                    <h1>{card['icon']} {card['value']}</h1>
                </div>
                """, unsafe_allow_html=True)
# Sub header style
subheader_style = """
<style>
.subheader-container {
    background-color: #2258a9;
    color: white; 
    padding: 10px;
    max-width: 50%;
    font-size: 24px;
    text-align: center;
    border-radius: 4px;
    margin: 40px 0;
    margin-left: auto;
    margin-right: auto;
}
</style>
"""
st.markdown(subheader_style, unsafe_allow_html=True)
st.markdown(f'<div class="subheader-container">GDP Dynamics and Insights</div>', unsafe_allow_html=True)

# Create a grid of 2 boxes for GDP visualization
cola, colb = st.columns(2)
with cola:
    last_six_years = gdp_macro_economy[gdp_macro_economy['Year'] >= (2022-5)]
    sector_data_last_six_years = sector_gdp[sector_gdp['Year'].isin(last_six_years['Year'])]
    # Create the figure
fig = go.Figure()

# Add bar chart for each sector
fig.add_trace(go.Bar(
    x=sector_data_last_six_years['Year'],
    y=sector_data_last_six_years['AGRICULTURE, FORESTRY & FISHING'],
    name='Agriculture, Forestry & Fishing',
    marker_color='orange'
))
fig.add_trace(go.Bar(
    x=sector_data_last_six_years['Year'],
    y=sector_data_last_six_years['INDUSTRY'],
    name='Industry',
    marker_color='grey'
))
fig.add_trace(go.Bar(
    x=sector_data_last_six_years['Year'],
    y=sector_data_last_six_years['SERVICES'],
    name='Services',
    marker_color='brown'
))
fig.add_trace(go.Bar(
    x=sector_data_last_six_years['Year'],
    y=sector_data_last_six_years['TAXES LESS SUBSIDIES ON PRODUCTS'],
    name='Taxes less subsidies on products',
    marker_color='yellow'
))

# Add line chart for growth rate
fig.add_trace(go.Scatter(
    x=last_six_years['Year'],
    y=last_six_years['Growth rate'],
    name='Growth Rate',
    mode='lines+markers',
    line=dict(color='black', dash='dash')
))

# Update the layout for a stacked bar chart
fig.update_layout(barmode='stack')

# Display the figure in Streamlit
st.plotly_chart(fig)



st.markdown(subheader_style, unsafe_allow_html=True)
st.markdown(f'<div class="subheader-container">Insights On the Consumer Price Index</div>', unsafe_allow_html=True)
