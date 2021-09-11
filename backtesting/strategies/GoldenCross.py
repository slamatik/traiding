import csv
import backtrader as bt
import math
import yfinance as yf
import pandas as pd
from time import time

data = yf.download('spy', period='1y', interval='1h')
data.to_csv('data.csv')

"""
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
"""


class GoldenCrossStrategy(bt.Strategy):
    params = (
        ('fast', 21),
        ('slow', 50),
        ('pct', 0.95),
        ('printlog', True)
    )

    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.fast_ma = bt.indicators.MovingAverageSimple(self.data.close, period=self.params.fast)
        self.slow_ma = bt.indicators.MovingAverageSimple(self.data.close, period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)

        self.size = None

        self.data_frame = {'fast': [], 'slow': [], 'res': []}

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log(f'BUY EXECUTED, '
                             f'Price: {order.executed.price:.2f}, '
                             f'Cost: {order.executed.value:.2f}, '
                             f'Comm: {order.executed.comm:.2f}')
                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                elif order.issell():
                    self.log(f'SELL EXECUTED, '
                             f'Price: {order.executed.price:.2f}, '
                             f'Cost: {order.executed.value:.2f}, '
                             f'Comm: {order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        print(f'Bars Held: {trade.barlen}')
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}')

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                amount = self.params.pct * self.broker.cash
                self.size = math.floor(amount / self.data.close)
                # self.log(f'BUY {self.size} at {self.data.close[0]}')
                self.order = self.buy(size=self.size)
        else:
            if self.crossover < 0:
                # self.log(f'SELL {self.size} at {self.data.close[0]}')
                self.order = self.sell(size=self.size)
                self.size = None

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    # def stop(self):
    #     with open('results.csv', 'a') as f:
    #         writer = csv.writer(f, dialect='excel')
    #         writer.writerow([self.params.fast, self.params.slow, self.broker.get_value()])
    #
    #     # self.log(f'Slow MA {self.params.slow}, Fast MA {self.params.fast}, Ending Value {self.broker.cash}',
    #     #          doprint=True)


t0 = time()

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # strats = cerebro.optstrategy(GoldenCrossStrategy,
    #                              fast=range(5, 51, 5), slow=range(50, 101, 5))
    cerebro.addstrategy(GoldenCrossStrategy)

    # Create a Data Feed
    data = bt.feeds.YahooFinanceData(dataname='data.csv')
    cerebro.adddata(data)

    cerebro.broker.setcash(1000)
    # cerebro.broker.setcommission(0)

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()

print(f'Time taken: {time() - t0:.2f}')
