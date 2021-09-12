import sqlite3
import pandas as pd

data = pd.read_csv(r'C:\Users\slama\PycharmProjects\traiding\markets\sp500.csv')


def connect():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("""create table if not exists stock (
                id integer PRIMARY KEY,
                ticker text not null UNIQUE,
                name text not null
                )""")
    c.execute("select * from stock")
    row = c.fetchone()
    if not row:
        print('Table is empty... populating tickers...')
        for idx, row in data.iterrows():
            try:
                c.execute(f"INSERT INTO stock (ticker, name) values (?,?)", (row.Symbol, row.Company))
            except Exception as e:
                print(row.Symbol)
                print(e)

    conn.commit()
    conn.close()


def insert(ticker, name):
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    try:
        c.execute(f"INSERT INTO stock (ticker, name) values (?,?)", (ticker, name))
    except Exception as e:
        print(ticker)
        print(e)

    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute("select * from stock")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_all():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute('delete from stock')
    conn.commit()
    conn.close()
