import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

#Option to text just python part, excluding streamlit code
lit = True

#reading csv:s to dataframes
df_price = pd.read_csv("Electricity_price_2015-2025.csv", sep =";", decimal = ",")
df_cons = pd.read_csv("Electricity_consumption_2015-2025.csv")

#Drop missing values
df_price = df_price.dropna()
df_cons = df_cons.dropna()

#changing times to pd.datetimes
df_price['timestamp'] = pd.to_datetime(df_price['timestamp'])
df_cons['time'] = pd.to_datetime(df_cons['time'])
df_cons.rename(columns = {'time': 'timestamp'}, inplace = True)

#Merging two dataframes
df = pd.merge(df_price, df_cons, on = 'timestamp')

#renaming columns to lower case
df.rename(columns = {'Price': 'price', 'kWh' : 'kwh','Temperature' : 'temperature'}, inplace = True)


#Forming hourly rate from price and Kwh per hour
df['total_price'] = df['price'] * df['kwh']

""" #Forming date and month columns so we can aggregate values later
df['day'] = pd.to_datetime(df['timestamp']).dt.date
df['month'] = df['timestamp'].dt.to_period('M')


#Forming new dfs to show hourly, daily and monthly values
df_hourly = df.groupby(['timestamp'], as_index = False).agg({'Price' : 'mean', 'kWh' : 'sum', 'Temperature' : 'mean'})
df_daily = df.groupby(['day'], as_index= False).agg({'Price' : 'mean', 'kWh' : 'sum', 'Temperature' : 'mean'})
df_monthly = df.groupby(['month'], as_index= False).agg({'Price' : 'mean', 'kWh' : 'sum', 'Temperature' : 'mean'})

#Renaming columns to match hourly, daily and monthly data
df_hourly.rename(columns = {'Price' : 'mean_price', 'kWh' : 'total_kwh', 'Temperature' : 'mean_temperature', 'timestamp': 'hour'}, inplace = True)
df_daily.rename(columns = {'Price' : 'mean_price', 'kWh' : 'total_kwh', 'Temperature' : 'mean_temperature'}, inplace = True)
df_monthly.rename(columns = {'Price' : 'mean_price', 'kWh' : 'total_kwh', 'Temperature' : 'mean_temperature'}, inplace = True)

#Forming total_consumption column to all dataframes
df_hourly['total_consumption'] = df_hourly['mean_price'] * df_hourly['total_kwh']

df_daily['total_consumption'] = df_daily['mean_price'] * df_daily['total_kwh']
df_monthly['total_consumption'] = df_monthly['mean_price'] * df_daily['total_kwh'] """


if lit:

    option = st.selectbox(
        "Choose time interval",
        ['Hourly','Daily','Monthly']
    )

    if option == 'Daily':
        grouped_df = df.groupby(df['timestamp'].dt.date).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})

    elif option == 'Monthly':
        grouped_df = df.groupby(df['timestamp'].dt.to_period('M')).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})
        
    else:
        grouped_df = df

    st.write(grouped_df)
