import yfinance as yf
import pandas as pd
import sqlite3

conn = sqlite3.connect('stocks.db')
c = conn.cursor()


def view():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("select * from stock")
    rows = c.fetchall()
    conn.close()
    return rows

tickers = ['msft', 'aapl']