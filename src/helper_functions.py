import requests, math
from bs4 import BeautifulSoup
import spacy
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import time

def prices(symbol: str):
    "Retuns a data frame of stock price information."
    
    # creating empty stock info dictionary
    stock_data = {
    'Company': [],
    'Symbol': [],
    'currentPrice': [],
    'dayHigh': [],
    'dayLow': [],
    '52wkHigh': [],
    '52wkLow': [],
    'dividendRate': []
    }
    # appending data from yf
    stock_info = yf.Ticker(symbol).info
    stock_data['Company'].append(stock_info['shortName'])
    stock_data['Symbol'].append(stock_info['symbol'])
    stock_data['currentPrice'].append(stock_info['currentPrice'])
    stock_data['dayHigh'].append(stock_info['dayHigh'])
    stock_data['dayLow'].append(stock_info['dayLow'])
    stock_data['52wkHigh'].append(stock_info['fiftyTwoWeekHigh'])
    stock_data['52wkLow'].append(stock_info['fiftyTwoWeekLow'])            
            
    # converting dividend None types to floats
    dividend = stock_info['dividendRate']
    if dividend != None:
        dividend = dividend
    else:
        dividend = 0
    stock_data['dividendRate'].append(dividend)
    
    return pd.DataFrame(stock_data)