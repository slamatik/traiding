import yfinance as yf
import sqlite3
import time
import pandas as pd
import os


# todo get more data,
#  add table with intraday values look for ways to automate data collection on daily basis (1min, 5mmin, 15mmin, 1hr, 4hr, 1d)


def connect():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists stock_price (
        id integer primary key,
        stock_id integer,
        date not null,
        open not null,
        high not null,
        low not null,
        close not null,
        volume not null,
        adjusted_close not null,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )""")
    conn.commit()
    conn.close()


def get_ticker_names():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("SELECT id, ticker from stock")
    row = c.fetchall()
    return row


def get_prices():
    connect()
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    names = get_ticker_names()
    interval = 50

    for i in range(0, len(names), interval):
        print(f'Stage {i}')
        names_slice = names[i:i + interval]
        ticker_slice = [i[1] for i in names_slice]
        idx_slice = [i[0] for i in names_slice]
        df = yf.download(ticker_slice, group_by='ticker')

        for idx in range(len(names_slice)):
            temp_df = df[ticker_slice[idx]].dropna()
            for date, row in temp_df.iterrows():
                c.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, adjusted_close)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                idx_slice[idx], date.__str__(), row.Open, row.High, row.Low, row.Close, row.Volume, row['Adj Close']))
        time.sleep(10)

        # for col in df.columns.levels[0]:
        #     temp_df = df[col]
        #     for date, row in temp_df.iterrows():
        #         c.execute("""
        #         INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, adjusted_close)
        #         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        #         """, (idx, date.__str__(), row.Open, row.High, row.Low, row.Close, row.Volume, row['Adj Close']))

    # for (idx, ticker) in names:
    #     print(f'Working on {ticker}...')
    #     data = yf.download(ticker)
    #     for date, row in data.iterrows():
    #         c.execute("""
    #         INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, adjusted_close)
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    #         """, (idx, date.__str__(), row.Open, row.High, row.Low, row.Close, row.Volume, row['Adj Close']))
    conn.commit()
    conn.close()


t0 = time.time()
get_prices()
print(time.time() - t0)

# names = get_ticker_names()
# print(names)
# ids = [i[0] for i in names]
# print(ids)
# names = [i[1] for i in names]
# print(names)
# print(len(names))
# for i in range(0, len(names), 100):
#     print(range(i, i + 100))
