import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup


start = '2022-01-01'
current = datetime.datetime.now()

def data_load(crypto):
    data = yf.download(crypto, start, current)
    data.reset_index(inplace=True)
    return data

bitcoin = data_load('BTC-USD')
litecoin = data_load('LTC-USD')
dogecoin = data_load('DGC-USD')
ethereum = data_load('ETH-USD')
ripple = data_load('XRP-USD')

def get_bitcoin():
    bitcoin_volume = bitcoin.iloc[-1].loc['Volume']
    bitcoin_current_price = bitcoin.iloc[-1].iloc[4]
    return bitcoin_volume, bitcoin_current_price

def get_litecoin():
    # Your code to fetch bitcoin data from API

    litecoin_volume = litecoin.iloc[-1].loc['Volume']
    litecoin_current_price = litecoin.iloc[-1].iloc[4]
    return litecoin_volume, litecoin_current_price

def get_dogecoin():
    # Your code to fetch bitcoin data from API
    dogecoin_volume = dogecoin.iloc[-1].loc['Volume']
    dogecoin_current_price = dogecoin.iloc[-1].iloc[4]
    return dogecoin_volume, dogecoin_current_price

def get_ethereum():
    ethereum_volume = ethereum.iloc[-1].loc['Volume']
    ethereum_current_price = ethereum.iloc[-1].iloc[4]
    return ethereum_volume, ethereum_current_price

def get_ripple():
    # Your code to fetch bitcoin data from API
    ripple_volume = ripple.iloc[-1].loc['Volume']
    ripple_current_price = ripple.iloc[-1].iloc[4]

    return ripple_volume, ripple_current_price
def get_current_data():
    bitcoin_volume, bitcoin_current_price = get_bitcoin()
    litecoin_volume, litecoin_current_price = get_litecoin()
    dogecoin_volume, dogecoin_current_price = get_dogecoin()
    ethereum_volume, ethereum_current_price = get_ethereum()
    ripple_volume, ripple_current_price = get_ripple()
    context = {
        'bitcoin_volume': bitcoin_volume/1000000000,
        'bitcoin_current_price': bitcoin_current_price/1000,
        'litecoin_volume': litecoin_volume/10000000,
        'litecoin_current_price': litecoin_current_price,
        'dogecoin_volume': dogecoin_volume/1000,
        'dogecoin_current_price': dogecoin_current_price,
        'ethereum_volume': ethereum_volume/1000000000,
        'ethereum_current_price': ethereum_current_price/1000,
        'ripple_volume': ripple_volume/10000000000,
        'ripple_current_price': ripple_current_price,
    }
    
    return context

def fetch_news():
    url = 'https://www.coindesk.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select('div.kuxwiI > div')  # Adjust selector to match actual structure

    news_data = []

    for article in articles:
        author = article.select_one('div.gJMKuU a')
        if author:
            data = {
                'headline': article.select_one('h3').text.strip() if article.select_one('h3') else article.select_one('h6').text.strip(),
                'summary': article.select_one('p').text.strip(),
                'author': author.text.strip(),
                'time': article.select_one('div.eeyqKG span').text.strip(),
                'link': url + article.select_one('a.card-title-link')['href'].strip()
            }
            news_data.append(data)

    return news_data