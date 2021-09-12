import backtrader as bt
import yfinance as yf
import pandas_datareader as pdr

data = pdr.get_data_yahoo('AAPL')
print(data)

#
# data = yf.download('nio', period='5d', interval='60m')
# data.to_csv('data.csv')
#
# class TestStrategy(bt.Strategy):
#
#     def log(self, txt, dt=None):
#         """Logging function for this strategy"""
#         dt = dt or self.datas[0].datetime.date(0)
#         print(f'{dt.isoformat()}, {txt}')
#
#     def __init__(self):
#         self.dataclose = self.datas[0].close
#
#
#     def next(self):
#         # self.log(f'Close {self.dataclose[0]:.2f}')
#         self.log(self.dataclose[0])
#
# if __name__ == '__main__':
#     cerebro = bt.Cerebro()
#     cerebro.broker.setcash(100000.0)
#     cerebro.addstrategy(TestStrategy)
#     print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
#
#     data = bt.feeds.YahooFinanceData(dataname='data.csv')
#     cerebro.adddata(data)
#
#     cerebro.run()
#
#     print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
