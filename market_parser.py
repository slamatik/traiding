import pandas as pd
import pandas_ta as ta
import yfinance as yf
from signal_functions import *
from helper import *

# update_data()
data, names = read_data_csv('sp')

# for ticker in pd.read_csv('markets/sp500.csv').Symbol:
#     df = build_df(ticker, data, names)
#     # print(df)
#     # break
#     for idx in range(1, len(df)):
#         if bullish_engulfing(df, idx):
#             print(ticker, df.iloc[idx].Date)

for ticker in pd.read_csv('markets/sp500.csv').Symbol:
    df = build_df(ticker, data, names)
    if is_consolidating(df, 2):
        print(ticker)