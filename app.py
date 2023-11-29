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
st.dataframe(gdp_macro_economy)

gdp_expenditure = pd.read_excel(
    io="GDP_data.xlsx",
    engine="openpyxl",
    sheet_name="T3 GDP CY"
)
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

st.dataframe(quarterly_gdp)
## Loading CPI data file
cpi_urban = pd.read_excel(
    io="CleanedCPI.xlsx",
    engine="openpyxl",
    sheet_name="Urban"
)
st.dataframe(cpi_urban)
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
    # Calculate the total GDP for each year for hover information
    sector_data_last_six_years['Total GDP'] = sector_data_last_six_years[['AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY', 'SERVICES', 'TAXES LESS SUBSIDIES ON PRODUCTS']].sum(axis=1)



    fig = go.Figure()
    # Add stacked bar chart for each sector
   
    sectors = ['AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY', 'SERVICES', 'TAXES LESS SUBSIDIES ON PRODUCTS']
    colors = ['orange', 'grey', 'brown', 'yellow'] # Adjust the colors as needed

    for sector, color in zip(sectors, colors):
    # Calculate the percentage for hover as a string
        sector_percentage = ((sector_data_last_six_years[sector] / sector_data_last_six_years['Total GDP']) * 100).astype(str)

    # Create hovertemplate string with percentage included
        hovertemplate = ['%{y:.2f} billion RWF<br>' + sector + '<br>' + perc + '%' for perc in sector_percentage]

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
            title='Real GDP Growth (2017 - 2022)',
        yaxis=dict(
            tickmode='auto',
            tickformat=',.1f',  # This will format the tick as a floating number with two decimal places
            title='GDP (in billion RWF)'
        ),
            xaxis=dict(tickmode='array', tickvals=sector_data_last_six_years['Year']),
            plot_bgcolor='white',  # Set background color to white for better readability
        )

        # Display the figure in Streamlit
    st.plotly_chart(fig)

with colb:
    # Filter data to the last six years up to 2022
    gdp_growth_data = gdp_macro_economy[gdp_macro_economy['Year'] >= (2022-5)]

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
        title='GDP Growth Rate (2017 - 2022)',
        xaxis_title='Year',
        yaxis_title='Growth Rate (%)',
        plot_bgcolor='white'
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)


st.markdown(subheader_style, unsafe_allow_html=True)
st.markdown(f'<div class="subheader-container">Insights On the Consumer Price Index</div>', unsafe_allow_html=True)


st.markdown(subheader_style, unsafe_allow_html=True)
st.markdown(f'<div class="subheader-container">Comparisons of GDP and CPI Data</div>', unsafe_allow_html=True)

colx, coly = st.columns(2)

with colx:
    # 1. Aggregate the CPI data to yearly by averaging
    cpi_urban['Year'] = pd.to_datetime(cpi_urban['Month']).dt.year
    yearly_cpi = cpi_urban[cpi_urban['Year'].between(2017, 2022)].groupby('Year')['GENERAL INDEX (CPI)'].mean()


    # 2. Calculate the yearly CPI rate as percentage change
    cpi_rate = yearly_cpi.pct_change().dropna() * 100  # Remove the first NaN value


    # 3. Extract the GDP deflator rate for 2017-2022
    gdp_deflator_rate = gdp_macro_economy[gdp_macro_economy['Year'].between(2017, 2022)]['Growth rate.2']


    # 4. Plot the time series line chart
    fig = go.Figure()


    # Add GDP Deflator Rate
    fig.add_trace(go.Scatter(
        x=gdp_deflator_rate.index,
        y=gdp_deflator_rate,
        mode='lines+markers',
        name='GDP Deflator Rate',
        line=dict(color='purple')  # or any color you prefer
    ))


    # Add CPI Rate
    fig.add_trace(go.Scatter(
        x=cpi_rate.index,
        y=cpi_rate,
        mode='lines+markers',
        name='CPI Rate',
        line=dict(color='red')  # or any color you prefer
    ))


    # Update layout to match the expected output
    fig.update_layout(
        title='GDP Deflator Rate vs CPI Rate (2017 - 2022)',
        xaxis=dict(
            title='Year',
            tickmode='linear',
            tickvals=list(range(2017, 2023))
        ),
        yaxis=dict(
            title='Rate (%)',
            tickmode='linear',
            range=[min(min(gdp_deflator_rate), min(cpi_rate)), max(max(gdp_deflator_rate), max(cpi_rate))],
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black'
        ),
        plot_bgcolor='white'
    )


    # Display the figure in Streamlit
    st.plotly_chart(fig)
