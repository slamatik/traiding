import backtrader as bt
import talib as ta
import yfinance as yf

# todo find candlestick patterns

yf.download('NIO', period='1y').to_csv('data.csv')


class Golden(bt.Strategy):
    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.candle = bt.talib.CDLHAMMER(self.data.open, self.data.high, self.data.low, self.data.close)
        self.macd = bt.indicators.MACD()

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

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    def next(self):
        if self.order: return

        if not self.position:

            print(self.macd.signal[0])
            print(self.macd.macd[0])


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Golden)
    # Create a Data Feed
    data = bt.feeds.YahooFinanceData(dataname='data.csv')
    cerebro.adddata(data)

    cerebro.broker.setcash(1000)
    # cerebro.broker.setcommission(0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=5)

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()
