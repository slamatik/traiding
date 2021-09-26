import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
import sqlite3

conn = sqlite3.connect('stocks.db')
c = conn.cursor()


# def view():
#     conn = sqlite3.connect('stocks.db')
#     c = conn.cursor()
#     c.execute("select * from stock")
#     rows = c.fetchall()
#     conn.close()
#     return rows
#
# c.execute('drop table if exists test')
#
# tickers = ['MSFT', 'AAPL']
# idxs = [13, 127]
# df = yf.download(tickers, group_by='ticker')
#
# for idx in range(len(tickers)):
#     temp_df = df[tickers[idx]].dropna()
#     temp_df['ticker'] = tickers[idx]
#     temp_df['ticker_id'] = idxs[idx]
#     temp_df.to_sql('test', conn, if_exists='append')
#
# # df.MSFT.to_sql('test', conn, if_exists='append')
# conn.commit()
# conn.close()