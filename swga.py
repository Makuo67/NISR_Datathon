import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go


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

    fig, ax = plt.subplots(figsize=(12, 6))  # Increase the width of the chart

    ax.plot(sectors_df['AGRICULTURE, FORESTRY & FISHING'], color='green')
    ax.plot(sectors_df['INDUSTRY'], color='blue')
    ax.plot(sectors_df['SERVICES'], color='orange')
    ax.plot(sectors_df['Taxes less subsidies on products'], color='purple')

    ax.set_title(
        'GDP By Sector Time-Series Analysis at Constant Price(2017)', fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage(%)')

    x_labels = sectors_df['Quarters']
    unique_quarters = x_labels[0::4].str.split().str[0].unique()
    x_ticks = np.arange(len(x_labels))

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=90)
    ax.set_xticks(x_ticks[::4])
    ax.set_xticklabels(unique_quarters, rotation=90)

    green_patch = mpatches.Patch(color='green', label=agriculture, linewidth=2)
    blue_patch = mpatches.Patch(color='blue', label=industry, linewidth=2)
    orange_patch = mpatches.Patch(
        color='orange', label=services, linewidth=2)
    purple_patch = mpatches.Patch(
        color='purple', label=taxes_and_less, linewidth=2)

    # Move the legend outside the chart using bbox_to_anchor
    legend = ax.legend(handles=[green_patch, blue_patch, orange_patch, purple_patch],
                       loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(axis='x', linestyle='--', linewidth=0.5)
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    # Add percentage sign at the top edge of the y-axis
    ax.annotate('%', fontsize=10, xy=(0, 1.02),
                xycoords=('axes fraction', 'axes fraction'))

    plt.tight_layout()

    st.pyplot(fig)

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

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green', 'blue', 'orange', 'purple']  # Colors for each sector
    for i, (col, color) in enumerate(zip(gdp_columns, colors), start=1):
        ax.plot(avg_quarterly_GDP['Quarter'], avg_quarterly_GDP[col],
                marker='o', linestyle='-', label=f'{col} - Trace {i}', color=color)

    ax.set_title('Quarterly GDP Trend for ' + selected_label,
                 fontsize=18, fontweight='bold')
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xticks(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.tick_params(axis='both', which='major', labelsize=10)

    legend = ax.legend(loc='upper left', bbox_to_anchor=(
        1.05, 1), borderaxespad=0.)

    # Add Frw(Billion) at the top edge of the y-axis
    ax.annotate('Frw(Billion)', fontsize=10, xy=(0, 1.02),
                xycoords=('axes fraction', 'axes fraction'))

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Increase the width of the chart
    fig.subplots_adjust(right=0.8)

    # Display the plot in Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    display_sector_to_gdp_time_series_analysis()
    display_quarterly_gdp()
