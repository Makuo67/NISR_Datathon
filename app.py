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
# st.dataframe(gdp_macro_economy)

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

# st.dataframe(quarterly_gdp)
## Loading CPI data file
cpi_urban = pd.read_excel(
    io="CleanedCPI.xlsx",
    engine="openpyxl",
    sheet_name="Urban"
)
# st.dataframe(cpi_urban)
cpi_other_indices = pd.read_excel(
    io="CleanedCPI.xlsx",
    engine="openpyxl",
    sheet_name="Other_Indices"
)
st.dataframe(cpi_other_indices)

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
inflation_rate = ((cpi_urban['GENERAL INDEX (CPI)'].iloc[-1] /
                  cpi_urban['GENERAL INDEX (CPI)'].iloc[-13]) - 1) * 100
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
st.markdown(f'<div class="subheader-container">GDP Dynamics and Insights</div>',
            unsafe_allow_html=True)

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
    plot_bgcolor='white'
)

# Display the figure in Streamlit
st.plotly_chart(fig)


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
    plot_bgcolor='white'
)

# Display the figure in Streamlit
st.plotly_chart(fig)


# FY Trend
cpi_urban['Year'] = cpi_urban['Month'].dt.year
cpi_urban['Month_Name'] = cpi_urban['Month'].dt.month_name()

# Define a function to calculate the year-over-year change rate for each category
def calculate_change_rate(df, year, categories):
    current_year_data = df[df['Year'] == year].groupby('Month_Name').mean()
    previous_year_data = df[df['Year'] == year - 1].groupby('Month_Name').mean()

    # Assuming you want to compare October to October
    change_rates = {}
    for category in categories:
        current_value = current_year_data.loc['October', category]
        previous_value = previous_year_data.loc['October', category]
        change_rate = ((current_value - previous_value) / previous_value) * 100
        change_rates[category] = change_rate
    
    return change_rates

# Calculate change rates for the required years
categories = [
    'Food and non-alcoholic beverages', 'Alcoholic beverages and tobacco',
    'Clothing and footwear', 'Housing, water, electricity, gas and other fuels',
    'Furnishing', 'Health', 
    'Transport', 'Communication', 'Recreation and culture',	
    'Education', 'Restaurants and hotels', 'Miscellaneous goods and services'

]

# Calculate change rates for 2022/2023
change_rates_2022_2023 = calculate_change_rate(cpi_urban, 2023, categories)

# Convert to DataFrame for easier handling
change_rates_df = pd.DataFrame(list(change_rates_2022_2023.items()), columns=['Category', 'Change Rate'])

# Sort the DataFrame by 'Change Rate' in ascending order
change_rates_df.sort_values('Change Rate', inplace=True)

# Create the horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=change_rates_df['Change Rate'],
    y=change_rates_df['Category'],
    orientation='h',  # Horizontal bar chart
    text=change_rates_df['Change Rate'].apply(lambda x: f"{x:.2f}%"),  # Add text labels
    textposition='auto',  # Position the text at the end of bars
))

# Update layout
fig.update_layout(
    title='Year-over-Year Change in CPI (October,2022 - October,2023)',
    xaxis=dict(title='Change Rate (%)'),
    yaxis=dict(title='Category'),
    plot_bgcolor='white',
    showlegend=False,
)

# Display the figure in Streamlit
st.plotly_chart(fig)

st.markdown(subheader_style, unsafe_allow_html=True)
st.markdown(f'<div class="subheader-container">Comparisons of GDP and CPI Data</div>', unsafe_allow_html=True)
