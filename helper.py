import pandas as pd
import pandas_ta as ta
import yfinance as yf


def update_data():
    sp = pd.read_csv('markets/sp500.csv')
    df = yf.download(' '.join(sp.Symbol.values), period='3mo', interval='1d')
    cols = df.columns.get_level_values(0).unique()
    for col in cols:
        df[f'{col}'].to_csv(f'data/sp/{col}_sp.csv')


def read_data_csv(market):
    dates = pd.read_csv(f'data/{market}/open_{market}.csv').Date
    open_prices = pd.read_csv(f'data/{market}/open_{market}.csv')
    close_prices = pd.read_csv(f'data/{market}/close_{market}.csv')
    high = pd.read_csv(f'data/{market}/high_{market}.csv')
    low = pd.read_csv(f'data/{market}/low_{market}.csv')
    data = [dates, open_prices, close_prices, high, low]
    names = ['Date', 'Open', 'Close', 'High', 'Low']
    return data, names


def build_df(ticker, data, names):
    df = pd.DataFrame({'Date': data[0]})
    for i in range(1, 5):
        df[f'{names[i]}'] = data[i][ticker]
    df['ema50'] = df.ta.ema(length=50)
    return df
