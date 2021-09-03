import backtrader as bt


class BollingerBandsStrategy(bt.Strategy):
    # params = (
    #     (),
    # )

    def log(self, txt, dt=None):
        """Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        # Keep a reference to the 'close' line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Bollinger Bands Indicator
        self.bb = bt.indicators.BollingerBands()
        self.bb_top = self.bb.lines.top
        self.bb_mid = self.bb.lines.mid
        self.bb_bot = self.bb.lines.bot

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
        # Simply lof the closing price of the series from the reference
        # self.log(f'Close, {self.dataclose[0]}')

        # Check if an order is pending, if yes, we cannot send a 2nd one
        if self.order: return

        # Check if we are in the market
        if not self.position:

            # Not yet, we might buy if
            if self.dataclose[0] < self.bb_bot:
                self.log(f'BUY CREATE {self.dataclose[0]:.2f}')
                self.order = self.buy()
        else:
            # Already in the market, we might sell
            if self.dataclose[0] >= self.bb_mid:
                self.log(f'SELL CREATE, {self.dataclose[0]:.2f}')
                self.order = self.sell()
