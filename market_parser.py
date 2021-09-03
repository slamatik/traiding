import pandas as pd
import pandas_ta as ta
import yfinance as yf
from signal_functions import *
from helper import *

# todo Strategy backtesting: Backtrader

# update_data()
# data, names = read_data_csv('sp')
#
# for ticker in pd.read_csv('markets/sp500.csv').Symbol:
#     df = build_df(ticker, data, names)
#     # print(df)
#     # break
#     for idx in range(1, len(df)):
#         if bullish_engulfing(df, idx):
#             print(ticker, df.iloc[idx].Date)


# msft = yf.download('MSFT', period='1mo', interval='1d')

nio = pd.read_csv('backtesting/data.csv')
# nio['ema50'] = nio.ta.ema(length=50)

for idx in range(len(nio)):
    if bullish_engulfing(nio, idx):
        print(nio.iloc[idx][0])

# print(nio)

