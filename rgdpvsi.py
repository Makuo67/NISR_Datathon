import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

merged_data = pd.merge(yearly_cpi_filtered[['Year', 'GENERAL INDEX (CPI)', 'Inflation Rate']],
                       gdp_filtered[['Year', 'Growth rate.1']],
                       on='Year')

inflation_rate = 'Inflation Rate'


def display_realgdp_to_inflation():
    """Plot Real GDP to Inflation Rate
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(merged_data['Year'], merged_data['Inflation Rate'],
            marker='o', linestyle='-', color='red', label='Inflation Rate')

    ax.plot(merged_data['Year'], merged_data['Growth rate.1'],
            marker='o', linestyle='-', color='blue', label='Growth rate.1')

    ax.set_title(
        'Trend of Inflation Rate and Real GDP Growth Rate over the Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Rate Percentage(%)')
    ax.legend()

    ax.grid(True)

    st.pyplot(fig)


display_realgdp_to_inflation()
