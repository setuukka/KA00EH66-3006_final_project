import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, date, time

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
df['date'] = df['timestamp'].dt.date
df['week_year'] = df['timestamp'].dt.strftime('%Y/%U')
df['month'] = df['timestamp'].dt.strftime('%Y/%m')

#print(df)

if lit:
    st.set_page_config(layout="wide")

    with st.sidebar:

        start_date = st.date_input("Start date",
                    df['timestamp'].min())
        start_date = pd.to_datetime(start_date)
        if start_date < df['timestamp'].min():
            start_date = df['timestamp'].min()
            st.write(f"Do not choose date before {df['date'].min()}")
            


        end_date = st.date_input("End date",
                    df['timestamp'].max())
        end_date = pd.to_datetime(end_date)   
        if end_date > df['timestamp'].max():
            end_date = df['timestamp'].max()
            st.write(f"Do not choose date after {df['date'].max()}")

        option = st.radio(
        "Choose time interval",
        ['Daily','Monthly','Weekly']
        )

    df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]






    if option == 'Daily':
        grouped_df = df.groupby(df['date']).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})
        #grouped_df = df.groupby(df['date']).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})

    elif option == 'Monthly':
        #grouped_df = df.groupby(df['timestamp'].dt.to_period('M')).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})
        grouped_df = df.groupby(df['month']).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})
        
    elif option == 'Weekly':
        grouped_df = df.groupby(df['week_year']).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})
    
    else:
        grouped_df = df.groupby(df['date']).agg({'price': 'mean', 'kwh' : 'sum', 'temperature' : 'mean', 'total_price' : 'sum'})

    grouped_df = grouped_df.reset_index().rename(columns = {'date' : 'time', 'month' : 'time', 'week_year' : 'time'})

    #grouped_df = grouped_df.reset_index()
    st.write(grouped_df)
    #st.write(grouped_df.iloc[:, 0])
    st.line_chart(
        data = grouped_df,
        x = 'time',
        y = 'kwh'
    )