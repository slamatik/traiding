import backtrader as bt
import talib
import talib as ta
import pandas as pd


class BullishEnglusfingStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.Close = self.datas[0].close
        self.Open = self.datas[0].open
        self.High = self.datas[0].high
        self.Low = self.datas[0].low

        self.ema = bt.indicators.ExponentialMovingAverage(period=50)
        self.atr = bt.indicators.AverageTrueRange()

        self.sl = None
        self.tp = None

    def is_bearish_candlestick(self, open, close):
        return close < open

    def is_bullish_candlestick(self, open, close):
        return close > open

    def bullish_engulfing(self, open, close, yopen, yclose):
        if self.is_bearish_candlestick(yopen, yclose):
            if open < yclose and close > yopen:
                return True

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
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}')

    def next(self):
        yclose = self.data.close.get(ago=-1)[0]
        yopen = self.data.open.get(ago=-1)[0]
        if self.order:
            return
        if not self.position:
            if self.bullish_engulfing(self.Open[0], self.Close[0], yclose, yopen):
                self.log('buy')
                self.order = self.buy()
                self.sl = self.Close[0] - 0.25 * self.atr
                self.tp = self.Close[0] + 0.5 * self.atr

        else:
            if self.Close[0] >= self.tp or self.Close[0] <= self.sl:
                print('SELL')
                self.order = self.sell()
                self.sl = None
                self.tp = None
