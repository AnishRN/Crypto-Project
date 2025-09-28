import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import pandas as pd
import datetime
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from bs4 import BeautifulSoup
import requests
from .apis import *
from django.http import JsonResponse

btc_data = bitcoin
ltc_data = litecoin
dgc_data = dogecoin
xrp_data = ripple
eth_data = ethereum
##candlestick Plots
bitcoin_cdst = go.Candlestick(
    x=btc_data['Date'],
    open=btc_data['Open'],
    high=btc_data['High'],
    low=btc_data['Low'],
    close=btc_data['Close']
)
litecoin_cdst = go.Candlestick(
    x=ltc_data['Date'],
    open=ltc_data['Open'],
    high=ltc_data['High'],
    low=ltc_data['Low'],
    close=ltc_data['Close']
)
ethereum_cdst = go.Candlestick(
    x=eth_data['Date'],
    open=eth_data['Open'],
    high=eth_data['High'],
    low=eth_data['Low'],
    close=eth_data['Close']
)
dogecoin_cdst = go.Candlestick(
    x=dgc_data['Date'],
    open=dgc_data['Open'],
    high=dgc_data['High'],
    low=dgc_data['Low'],
    close=dgc_data['Close']
)
ripple_cdst = go.Candlestick(
    x=xrp_data['Date'],
    open=xrp_data['Open'],
    high=xrp_data['High'],
    low=xrp_data['Low'],
    close=xrp_data['Close']
)

##volume plots
btc_bar = go.Bar(
    x=btc_data['Date'],
    y=btc_data['Volume'],
    name='Volume',
    marker=dict(color='blue') 
)
ltc_bar = go.Bar(
    x=ltc_data['Date'],
    y=ltc_data['Volume'],
    name='Volume',
    marker=dict(color='blue') 
)
eth_bar = go.Bar(
    x=eth_data['Date'],
    y=eth_data['Volume'],
    name='Volume',
    marker=dict(color='blue') 
)
dgc_bar = go.Bar(
    x=dgc_data['Date'],
    y=dgc_data['Volume'],
    name='Volume',
    marker=dict(color='blue') 
)
xrp_bar = go.Bar(
    x=xrp_data['Date'],
    y=xrp_data['Volume'],
    name='Volume',
    marker=dict(color='blue')
)


##prepare model

def generate_forecasts(currency, period, timestamp):
    # Prepare training data and models for each cryptocurrency
    if currency == "BTC-USD":
        train_data = btc_data[['Date', 'Close']]
    elif currency == "LTC_USD":
        train_data = ltc_data[['Date', 'Close']]
    elif currency == "XRP-USD":
        train_data = xrp_data[['Date', 'Close']]
    elif currency == "DGC-USD":
        train_data = dgc_data[['Date', 'Close']]
    elif currency == "ETH-USD":
        train_data = eth_data[['Date', 'Close']]

    train_data = train_data.rename(columns={'Date': 'ds', 'Close': 'y'})
    model = Prophet()
    model.fit(train_data)
    
    if period == "Days":
        forecast_period = int(timestamp) * 1
    elif period == "Weeks":
        forecast_period = int(timestamp) * 7
    elif period == "Months":
        forecast_period = int(timestamp) * 30
    elif period == "Years":
        forecast_period = int(timestamp) * 365
    
    forecast_period = min(int(forecast_period), 1000)  # Limit forecast period to prevent overflow
    future = model.make_future_dataframe(periods=int(forecast_period))
    forecast = model.predict(future)
    
    print(forecast_period)
    return forecast, model

