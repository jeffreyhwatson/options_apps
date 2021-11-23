import os, sys, math
import requests
from bs4 import BeautifulSoup
import spacy
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import dataframe_image as dfi
from datetime import datetime
import time

#  setting path
gparent = os.path.join(os.pardir)
sys.path.append(gparent)

def get_prices(symbol: str):
    "Retuns a data frame of stock price information."
    
    # creating empty stock info dictionary
    stock_data = {
    'Company': [],
    'Symbol': [],
    'Current Price': [],
    'Intraday High': [],
    'Intraday Low': [],
    '52wkHigh': [],
    '52wkLow': [],
    'Dividend': []
    }
    # appending data from yf
    stock_info = yf.Ticker(symbol).info
    stock_data['Company'].append(stock_info['shortName'])
    stock_data['Symbol'].append(stock_info['symbol'])
    stock_data['Current Price'].append(stock_info['currentPrice'])
    stock_data['Intraday High'].append(stock_info['dayHigh'])
    stock_data['Intraday Low'].append(stock_info['dayLow'])
    stock_data['52wkHigh'].append(stock_info['fiftyTwoWeekHigh'])
    stock_data['52wkLow'].append(stock_info['fiftyTwoWeekLow'])            
            
    # converting dividend None types to floats
    dividend = stock_info['dividendRate']
    if dividend != None:
        dividend = dividend
    else:
        dividend = 0
    stock_data['Dividend'].append(dividend)
    
    return pd.DataFrame(stock_data)

def df_plot(df, plot_name=False):
    """Saves a plot of a data frame to the figure directory."""
    
    path = os.path.join(gparent,'figures',f'{plot_name}.png')
    dfi.export(df,f'{path}', max_rows=-1)
    
def get_expirations(symbol : str):
    stock = yf.Ticker(symbol)
    return stock.options

def options_mrkt(symbol : str, expiration : str, option : str):
    stock = yf.Ticker(symbol)
    current_price = stock.info['currentPrice']
    dividend = stock.info['dividendRate']
    url = ('https://www.treasury.gov/resource-center/'
    'data-chart-center/interest-rates/Pages/TextView.aspx?data=yield')
    rates = pd.read_html(url)
    risk_free_rate = rates[1]['3 mo']
    print(f"Current Price: ${current_price}")
    print(f"Dividend: ${dividend}")
    print(f"3 Month TBill Rate: {risk_free_rate.to_string().split()[1]}%")
    opt = stock.option_chain(expiration)
    if option == 'calls':
        return opt.calls.sort_values(by='strike')
    elif option == 'puts':
        return opt.puts.sort_values(by='strike')