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


def bear(candle):
    return candle.Close < candle.Open


def bull(candle):
    return candle.Close > candle.Open


def is_bullish_engulfing(df, idx):
    today = df.iloc[idx]
    today_1 = df.iloc[idx - 1]
    if bear(today_1) and today.Open < today_1.Close and today.Close > today_1.Open:
        return True
    return False


def build_df(ticker, data, names):
    df = pd.DataFrame({'Date': data[0]})
    for i in range(1, 5):
        df[f'{names[i]}'] = data[i][ticker]
    # print(df.ta.ema(length=50))
    df['ema50'] = df.ta.ema(length=50)
    return df


def below_ema(df, idx):
    return df.iloc[idx].Close < df.iloc[idx].ema50


# update_data()
data, names = read_data_csv('sp')

for ticker in pd.read_csv('markets/sp500.csv').Symbol:
    df = build_df(ticker, data, names)
    # print(df)
    # break
    for idx in range(1, len(df)):
        if below_ema(df, idx) and is_bullish_engulfing(df, idx):
            print(ticker, df.iloc[idx].Date)
