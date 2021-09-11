import backtrader as bt
import yfinance as yf
from time import time

from strategies.BollingerBands import BollingerBandsStrategy
from strategies.Hammer import HammerStrategy
from strategies.GoldenCross import GoldenCrossStrategy
from strategies.BullishEngulfing import BullishEnglusfingStrategy

# data = yf.download('ko', period='5y', interval='1d')
# data.to_csv('data.csv')

data = yf.download('spy', period='5y', interval='1d')
data.to_csv('data.csv')

t0 = time()

# TODO: Stochastic indicator https://community.backtrader.com/topic/2435/stochastic-strategy-with-tp-and-stop-loss-how-to-reverse-position-why-is-the-commission-not-calculated

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # strats = cerebro.optstrategy(GoldenCrossStrategy,
    #                              fast=range(5, 51, 5), slow=range(50, 101, 5))
    cerebro.addstrategy(BollingerBandsStrategy)
    # Create a Data Feed
    data = bt.feeds.YahooFinanceData(dataname='data.csv')
    cerebro.adddata(data)

    cerebro.broker.setcash(1000)
    # cerebro.broker.setcommission(0)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=5)

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()

print(f'Time taken: {time()  - t0:.2f}')