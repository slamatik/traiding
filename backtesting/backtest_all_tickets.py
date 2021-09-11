import backtrader as bt
import yfinance as yf
from time import time
import pandas as pd

from strategies.GoldenCross import GoldenCrossStrategy


results = {'ticker': [], 'cash': [], 'value': []}

t0 = time()

for ticker in pd.read_csv(r'C:\Users\slama\PycharmProjects\traiding\markets\sp500.csv').Symbol:

    t1 = time()

    yf.download(ticker, period='5y', interval='1d').to_csv('data.csv')
    data = bt.feeds.YahooFinanceData(dataname='data.csv')

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000)
    cerebro.addstrategy(GoldenCrossStrategy)
    cerebro.adddata(data)

    cerebro.run()

    results['ticker'].append(ticker)
    results['cash'].append(cerebro.broker.cash)
    results['value'].append(cerebro.broker.getvalue())

    # print(f'{ticker} completed. Time taken: {time() - t1:.2f}')

    # break

print(f'Total time taken: {time() - t0:.2f} seconds')

pd.DataFrame(results).to_csv('results.csv')