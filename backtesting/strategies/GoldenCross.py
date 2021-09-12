import backtrader as bt
import math

from backtesting.main import run


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

    # for multiple datafeeds
    # def stop(self):
    #     with open('results.csv', 'a') as f:
    #         writer = csv.writer(f, dialect='excel')
    #         writer.writerow([self.params.fast, self.params.slow, self.broker.get_value()])
    #
    #     # self.log(f'Slow MA {self.params.slow}, Fast MA {self.params.fast}, Ending Value {self.broker.cash}',
    #     #          doprint=True)


if __name__ == '__main__':
    run(GoldenCrossStrategy, 'aapl')
