import backtrader as bt
import sqlite3
import pandas as pd


class PandasData(bt.feeds.PandasData):
    params = (
        ('datetime', 'date'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None)
    )


def get_data(ticker, last=None, between=None):
    if last:
        date_range = f" AND date > date('now', '-{last} years')"
    elif between:
        d0, d1 = between
        date_range = f" AND date BETWEEN date('{d0}-01-01') and date('{d1}-01-01')"
    conn = sqlite3.connect(r'C:\Users\slama\PycharmProjects\traiding\database\stocks.db')
    c = conn.cursor()
    c.execute(f"select id from stock where ticker='{ticker.upper()}'")
    stock_id = c.fetchone()[0]
    df = pd.read_sql_query(f"select * from stock_price where stock_id={stock_id}" + date_range, conn)
    conn.close()
    df.date = pd.to_datetime(df.date)
    df.set_index('date', drop=True, inplace=True)
    return df.drop(columns=['id', 'stock_id', 'adjusted_close'])


def run(strategy, name, cash=1000, years=5, plot=True):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy)
    # data = bt.feeds.YahooFinanceData(dataname=data)
    data = bt.feeds.PandasData(dataname=get_data(name, last=years))
    cerebro.adddata(data)
    cerebro.broker.setcash(cash)
    # cerebro.broker.setcommission(0)
    cerebro.run()
    print(f'Starting Portfolio Value: {cash}. Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    if plot:
        # cerebro.plot(fmt_x_ticks='%Y-%b-%d')
        cerebro.plot()

# TODO: Stochastic indicator https://community.backtrader.com/topic/2435/stochastic-strategy-with-tp-and-stop-loss-how-to-reverse-position-why-is-the-commission-not-calculated
