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

def inflation_by_category():
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
        title='Inflation Rate by Category (October,2022 - October,2023)',
        xaxis=dict(title='Change Rate (%)'),
        yaxis=dict(title='Category'),
        plot_bgcolor='white',
        showlegend=False,
        width=700
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)
    st.markdown("""
    <style>
    .food {
        color: #ffff;
        background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        width: 50%;
    }
    </style>
    <div class="food">
        Food and Non Alcoholic Beverages prices experienced significant inflation betwen Oct.2022 to Oct. 2023
    </div>
    """, unsafe_allow_html=True)