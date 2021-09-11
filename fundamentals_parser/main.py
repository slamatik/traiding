import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

import re
import pandas as pd
import yfinance as yf

# todo finish parsing all data

# data = pd.read_csv(r'C:\Users\slama\PycharmProjects\traiding\markets\sp500.csv')

msft = 'msft'

# msft = yf.Ticker('msft').info
#
# print(f'Low: {msft["targetLowPrice"]}'
#       f'Med : {msft["targetMedianPrice"]}'
#       f'Mean: {msft["targetMeanPrice"]}'
#       f'High: {msft["targetHighPrice"]}'
#       f'No Anal: {msft["numberOfAnalystOpinions"]}'
#       f'Rec mean: {msft["recommendationMean"]}'
#       f'Recom: {msft["recommendationKey"]}')

url = r'https://money.cnn.com/quote/forecast/forecast.html?symb=MSFT'
url = urlopen(url)
soup = BeautifulSoup(url, 'html.parser')
text = ''
for p in soup.find(id='wsod_forecasts').find_all('p'):
    text += p.text
pattern = r"""
(?P<analyst>\d+)
.*\bmedian\starget\sof\s(?P<median>\d+.\d+)
.*\shigh\sestimate\sof\s(?P<high>\d+.\d+)
.*\slow\sestimate\sof\s(?P<low>\d+.\d+)
.*estimate.*[+|-](?P<change>\d+.\d+)
.*last\sprice\sof\s(?P<last>\d+.\d+)
.*is\sto\s(?P<rating>\w+)
"""
match = re.finditer(pattern, text, flags=re.VERBOSE)
results = [i.groupdict() for i in match]
print(results)