import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from helper import *
# from xbbg import blp

df = pd.read_excel('BarLoader -.xlsx', engine='openpyxl', index_col=0)
# print(df.columns[7:])

for idx, row in df.iterrows():
    tickers = []
    for col in row[7::2]:
        if not type(col) == float:
            tickers.append(col)
    break

# tickers = ' '.join(tickers)
# print(tickers)

values = {}
for ticker in tickers:
    print(ticker)
    data = yf.Ticker(ticker).info['previousClose']
    values[ticker] = data

print(values)

fig, ax = plt.subplots()
ax.barh(tickers, [values[i] for i in tickers])
plt.show()