import plotly.express as px
import pandas as pd
import streamlit as st
import datetime

# Set Streamlit page configuration
st.set_page_config(
    page_title="DataDynamo Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# Load CPI data
cpi_df = pd.read_excel(
    io="CPI.xlsx",
    engine="openpyxl",
    sheet_name="All Rwanda"
)

# Rename the "Sector" column to "Year" for consistency
cpi_df = cpi_df.rename(columns={"Sector": "Year"})

# Load GDP data
gdp_df = pd.read_excel(
    io="GDP.xlsx",
    engine="openpyxl",
    sheet_name="CYGDP"
)

# Rename the "Sector" column to "Year" for consistency
gdp_df = gdp_df.rename(columns={"Sector": "Year"})

# Define the sidebar header and select boxes outside of the expander
st.sidebar.header("Please Filter Here: ")

cpi_category = None
gdp_sector = None

# Check if a CPI category is selected
if st.sidebar.checkbox("Filter CPI by Category"):
    cpi_category = st.sidebar.selectbox(
        "Select a CPI Category:",
        options=[col for col in cpi_df.columns if col not in [
            "Year", "GENERAL INDEX (CPI)"]]  # List available categories
    )

# Check if a GDP sector is selected
if st.sidebar.checkbox("Filter GDP by Sector"):
    gdp_sector = st.sidebar.selectbox(
        "Select a Sector for GDP:",
        options=[col for col in gdp_df.columns if col not in
                 ["Year", "GROSS DOMESTIC PRODUCT (GDP)", "Total population (millions)",
                  "GDP per head (in current US dollars)", "TAXES LESS SUBSIDIES ON PRODUCTS"]
                 ]  # List available sectors
    )

# Vary the style of the line graphs
line_styles = ["plotly", "plotly_dark",
               "plotly_white", "simple_white", "gridon"]
selected_style = st.sidebar.selectbox(
    "Select a Line Graph Style:", line_styles
)

# Display the title with emoji centered
st.markdown(
    '<div style="display: flex; justify-content: center;">'
    '<h1>&#x1F4CA; CPI and GDP DashBoard</h1>'  # Display a title with an emoji
    '<hr style="width: 100%; border: 1px solid #ccc;">'
    '</div>',
    unsafe_allow_html=True
)

# Define CSS styles for the boxes
box_style = "padding: 20px; text-align: center; background-color: #00a65a; border-radius: 10px; margin-bottom: 10px;"

# Create a grid of 2 boxes
cola, colb = st.columns(2)

# Box 1: Population (in million)
with cola:
    population_million = gdp_df['Total population (millions)'].iloc[-1]
    st.markdown(
        f'<div style="{box_style}">'
        f"<h3>{population_million:.2f} M</h3>"
        f"<p>Population (millions)</p>"
        '</div>',
        unsafe_allow_html=True
    )

# Box 2: Average Growth Rate
with colb:
    average_growth_rate = gdp_df['Growth rate'].mean()
    st.markdown(
        f'<div style="{box_style}">'
        f"<h3>{average_growth_rate:.2%}</h3>"
        f"<p>Average Growth Rate</p>"
        '</div>',
        unsafe_allow_html=True
    )

colc, cold = st.columns(2)
# Box 3: GDP per Capita (2022)
with colc:
    gdp_per_capita_2022 = gdp_df['GDP per head (in current US dollars)'].iloc[-1]
    st.markdown(
        f'<div style="{box_style}">'
        f"<h3>${gdp_per_capita_2022:,.2f}</h3>"
        f"<p>GDP per Capita (2022)</p>"
        '</div>',
        unsafe_allow_html=True
    )

# Box 4: Total GDP
with cold:
    total_gdp_2022 = gdp_df['GROSS DOMESTIC PRODUCT (GDP)'].iloc[-1]
    st.markdown(
        f'<div style="{box_style}">'
        f"<h3>Rwf {total_gdp_2022:,.2f} billion</h3>"
        f"<p> GDP (2022)</p>"
        '</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# Display "GROSS DOMESTIC PRODUCT (GDP)" line chart by default
st.markdown(
    '<div style="display: flex; justify-content: center;">'
    '<h3>RWANDA ANNUAL GDP GROWTH</h3>'
    '</div>',
    unsafe_allow_html=True
)
gdp_df_filtered = gdp_df[["Year", "GROSS DOMESTIC PRODUCT (GDP)"]]

fig_general_gdp = px.line(gdp_df_filtered, x="Year", y="GROSS DOMESTIC PRODUCT (GDP)",
                          labels={
                              "Year": "Year",
                              "GROSS DOMESTIC PRODUCT (GDP)": "GDP (in billion Rwf)"
                          },
                          template=selected_style
                          )
fig_general_gdp.update_traces(
    mode="lines+markers", marker=dict(size=8, color="blue"))
# Set the tickformat for the y-axis to display values in billions
fig_general_gdp.update_layout(
    width=800,
    yaxis_tickformat=".0f",
    margin=dict(l=200, r=100, t=0, b=0)
)
st.plotly_chart(fig_general_gdp, use_container_width=True)


# Plot the General CPI Index against the year
fig1 = px.area(cpi_df, x="Year", y="GENERAL INDEX (CPI)",
               labels={"Year": "Year", "GENERAL INDEX (CPI)": "CPI Index"}, template="gridon")
fig1.update_layout(
    margin=dict(l=200, r=100, t=0, b=0),
    width=800
)
st.markdown(
    '<div style="display: flex; justify-content: center;">'
    '<h3>Annual Change in CPI (Jan. 2009 - Nov. 2022)</h3>'
    '</div>',
    unsafe_allow_html=True
)
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Calculate GDP growth rate
    gdp_df['GDP Growth Rate'] = (gdp_df['GROSS DOMESTIC PRODUCT (GDP)'] /
                                 gdp_df['GROSS DOMESTIC PRODUCT (GDP)'].shift(1) - 1) * 100

    # Plot the GDP growth rate
    fig_gdp_growth = px.line(gdp_df, x="Year", y="GDP Growth Rate", title="GDP Growth Rate (2000-2022)",
                             labels={"Year": "Year",
                                     "GDP Growth Rate": "GDP Growth Rate (%)"}, template=selected_style)
    fig_gdp_growth.update_layout(
        title_x=0.3,  # Center the title horizontally
        title_font=dict(size=18),  # Adjust the font size as needed
    )
    st.plotly_chart(fig_gdp_growth, use_container_width=True)

with col2:
    # Calculate CPI inflation rate
    cpi_df['CPI Inflation Rate'] = (
        cpi_df['GENERAL INDEX (CPI)'] / cpi_df['GENERAL INDEX (CPI)'].shift(1) - 1) * 100

    # Plot the CPI inflation rate
    fig_cpi_inflation = px.line(cpi_df, x="Year", y="CPI Inflation Rate", title="Monthly CPI Inflation Rate (2009-2022)",
                                labels={
                                    "Year": "Year", "CPI Inflation Rate": "CPI Inflation Rate (%)"}, template=selected_style)
    fig_cpi_inflation.update_layout(
        title_x=0.3,  # Center the title horizontally
        title_font=dict(size=18),  # Adjust the font size as needed
    )
    st.plotly_chart(fig_cpi_inflation, use_container_width=True)

# Create two columns for layout
col4, col5 = st.columns(2)

with col4:
    # Filter the GDP data for the year 2022
    gdp_2022 = gdp_df[gdp_df["Year"] == 2022]

    # Specify the column names you want to include
    selected_sectors = [
        "TRADE &TRANSPORT",
        "AGRICULTURE, FORESTRY & FISHING",
        "INDUSTRY",
        "TOTAL MANUFACTURING",
        "SERVICES"
    ]

    # Create a new DataFrame for the bar chart
    bar_data = gdp_2022.melt(id_vars="Year", value_vars=selected_sectors,
                             var_name="Sector", value_name="GDP (in billion Rwf)")

    # Create a horizontal bar chart for GDP contribution by sector in 2022
    fig_gdp_2022 = px.bar(bar_data, x="GDP (in billion Rwf)", y="Sector",
                          labels={"x": "GDP (in billion Rwf)", "y": None},
                          title="GDP Contribution by Sector in 2022")
    fig_gdp_2022.update_layout(
        title_x=0.3,  # Center the title horizontally
        title_text="GDP Contribution by Sector in 2022",  # Your custom title
        title_font=dict(size=18),  # Adjust the font size as needed
    )

    # Set the orientation to horizontal
    fig_gdp_2022.update_layout(
        barmode="relative", xaxis_title="GDP (in billion Rwf)", yaxis_title="Sector")

    # Add text annotations with the percentage values
    total_gdp = bar_data["GDP (in billion Rwf)"].sum()
    percentage_values = (bar_data["GDP (in billion Rwf)"] / total_gdp) * 100

    fig_gdp_2022.update_traces(text=percentage_values.round(2).astype(str) + "%",
                               textposition="inside")

    # Show the bar chart
    st.plotly_chart(fig_gdp_2022, use_container_width=True)
    # Add margin to the right of col1 to create padding

with col5:
    # Load your GDP per head data
    gdp_per_head_data = gdp_df[[
        "Year", "GDP per head (in current US dollars)"]]

    # Define the period for displaying data points (every three years)
    period = 3

    # Create a figure using Plotly Express
    fig = px.area(gdp_per_head_data, x="Year", y="GDP per head (in current US dollars)",
                  labels={"Year": "Year",
                          "GDP per head (in current US dollars)": "GDP per head (US Dollars)"},
                  title="GDP per Capita (1999-2022)")
    fig.update_layout(
        title_x=0.3,  # Center the title horizontally
        title_font=dict(size=18),  # Adjust the font size as needed
    )

    # Add data points for every three-year period
    for year in gdp_per_head_data["Year"].unique():
        if (year - gdp_per_head_data["Year"].min()) % period == 0:
            data_point = gdp_per_head_data[gdp_per_head_data["Year"] == year]
            fig.add_trace(px.scatter(data_point, x="Year",
                                     y="GDP per head (in current US dollars)").data[0])

    # Customize the appearance of the data points
    fig.update_traces(marker=dict(size=8, color="red"), line=dict(width=1),
                      selector=dict(mode="markers+lines"), showlegend=False)

    # Show the graph using Streamlit
    st.plotly_chart(fig, use_container_width=True)

# From filter
if cpi_category:
    st.markdown(f"#### Annual Trend in CPI By Sector: {cpi_category}")
    cpi_df_filtered = cpi_df[["Year", cpi_category]]

    fig_selected = px.area(cpi_df_filtered, x="Year", y=cpi_category,
                           labels={"Year": "Year", cpi_category: "CPI Index"}, template=selected_style)
    st.plotly_chart(fig_selected, use_container_width=True)
    fig_selected.update_traces(line=dict(color='blue'), fill='tozeroy')
else:
    pass

# Display GDP line chart for the selected sector if a sector is selected
if gdp_sector:
    st.markdown(f"#### GDP GROWTH by Sector: {gdp_sector}")
    gdp_df_filtered = gdp_df[["Year", gdp_sector]]

    # Filter to omit rows with NaN values
    gdp_df_filtered = gdp_df_filtered[gdp_df_filtered[gdp_sector].notna()]

    fig_selected_gdp = px.area(gdp_df_filtered, x="Year", y=gdp_sector,
                               labels={"Year": "Year",
                                       gdp_sector: "GDP (in billion Rwf)"},
                               template=selected_style)
    st.plotly_chart(fig_selected_gdp, use_container_width=True)
else:
    pass
    # st.markdown(
    #     "### Please select a GDP sector from the sidebar to display the line chart.")
