import datetime
import math

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import argparse
import yfinance as yf


# yf.download('aapl', period='5y').to_csv('data_daily.csv')
# yf.download('aapl', period='5y').to_csv('data_weekly.csv')

class DoubleMACDStrategy(bt.Strategy):
    # params = (('pct', 0.95))

    def log(self, txt, dt=None):
        """Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.daily_macd = btind.MACD(self.data)
        self.weekly_macd = btind.MACD(self.data1)

        self.weekly_cross = bt.indicators.CrossOver(self.weekly_macd.macd, self.weekly_macd.signal, plot=True,
                                                    subplot=False)
        self.daily_cross = bt.indicators.CrossOver(self.daily_macd.macd, self.daily_macd.signal, plot=True,
                                                   subplot=False)

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.stop_loss = None

    # def nextstart(self):
    #     print('--------------------------------------------------')
    #     print('nextstart called with len', len(self))
    #     print('--------------------------------------------------')
    #
    #     super(SMAStrategy, self).nextstart()

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
        if self.order: return

        if not self.position:
            if self.weekly_cross == 1:
                amount = 0.95 * self.broker.cash
                size = math.floor(amount / self.data.close)
                self.log(f'WEEKLY MACD BUY CREATE of {size} at {self.data.open[0]}')
                self.order = self.buy(size=size)

            elif self.daily_cross == 1 and self.weekly_macd.macd > self.weekly_macd.signal:
                amount = 0.95 * self.broker.cash
                size = math.floor(amount / self.data.close)
                self.log(f'DAILY MACD BUY CREATE of {size} at {self.data.open[0]}')
                self.order = self.buy(size=size)

        else:
            if self.daily_cross == -1:
                self.stop_loss = self.data.low[-1]
                self.log(f'Daily crossover, sl set to {self.stop_loss}')

        if self.stop_loss:
            if self.data.close[0] <= self.stop_loss:
                self.log(f'STOP LOSS {self.data.close[0]}')
                self.order = self.sell(size=self.position.size)
                self.stop_loss = None


def printTradeAnalysis(analyzer):
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = (total_won / total_closed) * 100
    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print(f'SQN: {sqn}')


def runstart():
    args = parse_args()
    cerebro = bt.Cerebro()

    cerebro.addstrategy(DoubleMACDStrategy)

    # data = btfeeds.YahooFinanceData(dataname='data_daily.csv')
    data = btfeeds.YahooFinanceData(
        dataname=r'C:\Users\slama\PycharmProjects\traiding\backtesting\multiple timeframes\data_daily.csv')
    cerebro.adddata(data)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks, compression=1)

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

    cerebro.broker.setcash(10000)
    # cerebro.addwriter(bt.WriterFile, csv=True, out='aapl.csv')
    strategies = cerebro.run()
    firstStart = strategies[0]

    printTradeAnalysis(firstStart.analyzers.ta.get_analysis())
    printSQN(firstStart.analyzers.sqn.get_analysis())

    cerebro.plot(style='bars', volume=False)


def parse_args():
    parser = argparse.ArgumentParser(description='Multitimeframe Test')

    parser.add_argument('--dataname', default='', required=False, help='File Data to Load')
    parser.add_argument('--dataname2', default='', required=False, help='Larger timeframe file to load')
    parser.add_argument('--noresample', action='store_true', help='Do not resample, rather load larger timeframe')
    parser.add_argument('--timeframe', default='weekly', required=False, choices=['daily', 'weekly', 'monhtly'],
                        help='Timeframe to resample to')
    parser.add_argument('--compression', default=1, required=False, type=int, help='Compress n bars into 1')
    parser.add_argument('--indicators', action='store_true', help='Wether to apply Strategy with indicators')
    parser.add_argument('--onlydaily', action='store_true', help='Indicator only to be applied to daily timeframe')
    parser.add_argument('--period', default=10, required=False, type=int, help='Period to apply to indicator')

    return parser.parse_args()


if __name__ == '__main__':
    runstart()
