import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Sector Wise GDP Analysis')

df = pd.read_excel('data/CovertGDP.xlsx', sheet_name='QGDP SH')
df.drop(columns='Unnamed: 0', axis=1, inplace=True)
# df.set_index('Quarters', inplace=True)

sectors_df = df[['Quarters', 'AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY',
                'TRADE &TRANSPORT', 'OTHER SERVICES', 'Taxes less subsidies on products']]
st.dataframe(sectors_df)


# Step 1: Load the data
data = sectors_df.copy()

# Step 2: Preprocess the data
# Assuming the data contains columns 'Quarter' and sector names as the remaining columns

# Set 'Quarter' column as the index
data.set_index('Quarters', inplace=True)

# Step 3: Plot the time-series for each sector
st.title('Sector Time-Series Analysis')

for sector in data.columns:
    st.subheader(f'{sector} Sector')
    plt.figure(figsize=(50, 10))

    plt.subplot(2, 2, 1)
    sns.lineplot(data=data, x=data.index, y=data[sector])
    plt.xlabel('Quarters')
    plt.ylabel('Value')

    # Example: Area Plot
    # plt.subplot(2, 2, 1)
    # data[sector].plot.area()
    # plt.title(f'{sector} Area Plot')

    # plt.subplot(2, 2, 2)
    # data[sector].plot(kind='bar')
    # plt.title(f'{sector} Bar Plot')

    st.pyplot(plt)

# Step 4: Calculate the overall trend for each sector
trends = data.diff().mean()

# Step 5: Identify the growing, declining, and stable sectors
growing_sector = trends[trends > 0]
declining_sector = trends[trends < 0]
stable_sector = trends[trends == 0]

st.subheader('Trend Analysis')
st.write('Growing Sectors:')
st.write(growing_sector.index.tolist())

st.write('Declining Sectors:')
st.write(declining_sector.index.tolist())

st.write('Stable Sectors:')
st.write(stable_sector.index.tolist())


# for i, quarter in enumerate(data.index):
#     # Set the bottom starting point for stacking
#     bottom = 0 if i == 0 else data.iloc[i-1].values

#     plt.bar(data.columns, data.loc[quarter], label=quarter, bottom=bottom)

# plt.xlabel('Sectors')
# plt.ylabel('Value')
# plt.title('Stacked Bar Chart for Sectors Over Time')
# plt.legend()
# plt.xticks(rotation=45)
# st.pyplot(plt)
