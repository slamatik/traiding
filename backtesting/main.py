import backtrader as bt
import yfinance as yf

from strategies.BollingerBands import BollingerBandsStrategy
from strategies.Hammer import HammerStrategy

# data = yf.download('nio', period='1y', interval='1d')
# data.to_csv('data.csv')

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(HammerStrategy)
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
