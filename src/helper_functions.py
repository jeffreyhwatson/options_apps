import requests, math
from bs4 import BeautifulSoup
import spacy
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import time

def get_info(symbol: str):
    return yf.Ticker(symbol)