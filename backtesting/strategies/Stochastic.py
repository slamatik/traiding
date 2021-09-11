import backtrader as bt


class StochasticStrategy(bt.Strategy):
    def __init__(self):
        self.sto = bt.indicators.Stochastic()
        self.percD = self.sto.lines.percD
        self.percK = self.sto.lines.percK
