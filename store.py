
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel('data/CovertGDP.xlsx', sheet_name='QGDP SH')
df.drop(columns='Unnamed: 0', axis=1, inplace=True)

sectors_df = df[['Quarters', 'AGRICULTURE, FORESTRY & FISHING', 'INDUSTRY',
                'TRADE &TRANSPORT', 'OTHER SERVICES', 'Taxes less subsidies on products']]
# Step 1: Load the data
data = sectors_df.copy()

# Step 2: Preprocess the data
# Assuming the data contains columns 'Quarter' and sector names as the remaining columns

# Set 'Quarter' column as the index
data.set_index('Quarters', inplace=True)

# Step 3: Plot the time-series for each sector
st.title('Sector Time-Series Analysis')

# plt.style.use('seaborn-darkgrid')
plt.figure(figsize=(40, 20))

# Create a colormap for sectors
cmap = plt.cm.get_cmap('Accent')
colors = [cmap(i/len(data.columns)) for i in range(len(data.columns))]

# Plot all sectors on the same chart
for i, sector in enumerate(data.columns):
    sns.lineplot(data=data, x=data.index,
                 y=data[sector], label=sector, color=colors[i])

plt.xlabel('Quarter', fontsize=14)
plt.ylabel('Value', fontsize=14)
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1, 1), fontsize=12)
plt.title('Time-Series Analysis by Sector', fontsize=16)
plt.tight_layout()

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
