import plotly.express as px
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title=" GDP and CPI Dashboard",
    page_icon=":bar_chart:",
    layout="wide")
# CPI sheet
cpi_df = pd.read_excel(
    io="cpi.xlsx",
    engine="openpyxl",
    sheet_name="Consumer Price Index",
    skiprows=5,
    nrows=1000)

cpi_df = cpi_df.transpose()


# GDP Sheet
gdp_df = pd.read_excel(
    io="gdp.xlsx",
    engine="openpyxl",
    sheet_name="GDP",
    skiprows=0,
    nrows=1000)

gdp_df = gdp_df.transpose()
gdp_df.columns = gdp_df.iloc[0]
gdp_df.columns = [f"{col}{i+1}" if i >
                  0 else col for i, col in enumerate(gdp_df.columns)]
gdp_df = gdp_df[1:]

st.write("Consumer Price Index")
st.dataframe(cpi_df)
st.write("GDP")
st.dataframe(gdp_df)


# FIlter section
st.sidebar.header("Please Filter Here: ")
