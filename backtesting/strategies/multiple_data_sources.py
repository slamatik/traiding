import math
import yfinance as yf
import backtrader as bt
from datetime import datetime

# yf.download('aapl', period='5y', interval='1d').to_csv('aapl.csv')
# yf.download('msft', period='5y', interval='1d').to_csv('msft.csv')

class MACross(bt.Strategy):
    params = (
        ('slow', 50),
        ('fast', 21),
        ('oneplot', True),
        ('pct', 0.45)
    )

    def __init__(self):
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['slow'] = bt.indicators.MovingAverageSimple(d.close, period=self.params.slow)
            self.inds[d]['fast'] = bt.indicators.MovingAverageSimple(d.close, period=self.params.fast)
            self.inds[d]['cross'] = bt.indicators.CrossOver(self.inds[d]['fast'], self.inds[d]['slow'])

            if i > 0:
                if self.p.oneplot:
                    d.plotinfo.plotmaster = self.datas[0]

    def next(self):
        for i, d in enumerate(self.datas):
            dn = d._name
            pos = self.getposition(d).size
            if not pos:
                if self.inds[d]['cross'][0] == 1:
                    amount = self.params.pct * self.broker.cash
                    size = math.floor(amount / d.close[0])
                    self.buy(data=d, size=size)
            else:
                if self.inds[d]['cross'][0] == -1:
                    self.sell(data=d, size=pos)



        # for i, d in enumerate(self.datas):
        #     dt, dn = self.datetime.date(), d._name
        #     pos = self.getposition(d).size
        #     if not pos:
        #         if self.inds[d]['cross'][0] == 1:
        #             # amount = self.params.pct * self.broker.cash
        #             # size = math.floor(amount / d[0].close[0])
        #             self.buy(data=d, size=1)
        #         elif self.inds[d]['cross'][0] == -1:
        #             self.sell(data=d, size=1)
        #     else:
        #         if self.inds[d]['cross'][0] == 1:
        #             self.close(data=d)
        #             self.buy(data=d, size=1)
        #         elif self.inds[d]['cross'][0] == -1:
        #             self.close(data=d)
        #             self.sell(data=d, size=1)

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print(f'{dt} {trade.data._name} Closed: PnL Gross {trade.pnl:.2f}, Net {trade.pnlcomm:.2f}')


cerebro = bt.Cerebro()
cerebro.addstrategy(MACross, oneplot=False)
stocks = ['AAPL', 'MSFT']
for ticker in stocks:
    data = bt.feeds.YahooFinanceData(dataname=ticker+'.csv')
    cerebro.adddata(data)
startcash = 1000
cerebro.broker.setcash(startcash)
cerebro.run()
portvalue = round(cerebro.broker.getvalue(), 2)
pnl = portvalue - startcash
#Print out the final result
print('Final Portfolio Value: ${}'.format(portvalue))
print(cerebro.broker.cash)
print('P/L: ${}'.format(pnl))

#Finally plot the end results
cerebro.plot(style='candlestick')