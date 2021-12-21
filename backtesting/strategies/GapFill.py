import yfinance as yf
import backtrader as bt
import math
from datetime import datetime, time

from backtesting.main import run_simple


class GapFill(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.Close = self.datas[0].close
        self.Open = self.datas[0].open
        self.High = self.datas[0].high
        self.Low = self.datas[0].low

        self.yClose = self.datas[-1].close
        self.yOpen = self.datas[-1].open
        self.yHigh = self.datas[-1].high
        self.yLow = self.datas[-1].low

        self.order = None
        self.sl = None
        self.tp = None

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
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}, Bars Held: {trade.barlen}')

    def next(self):
        if self.order: return

        if not self.position:
            # print(self.data.datetime.time())
            if self.data.datetime.time() == time(hour=9, minute=30, second=00):
                print(self.data.datetime.date())
                print(f'Today Open: {self.Open[0]:.2f} --- Previous Close: {self.yClose[0]:.2f}')
                # if self.Open[0] > self.yClose[0]:
                #     self.log('GAP UP')
                #     print(f'Today Open: {self.Open[0]:.2f} --- Previous Close: {self.yClose[0]:.2f}')
                # if self.Open[0] < self.yClose[0]:
                #     self.log('GAP DOWN')
                #     print(f'Today Open: {self.Open[0]:.2f} --- Previous Close: {self.yClose[0]:.2f}')


run_simple(GapFill, r'C:\Users\slama\PycharmProjects\traiding\backtesting\AAPL_1min_2weeks.csv')
