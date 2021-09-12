class Ticker:
    def __init__(self, ticker: str, open: float, high: float, low: float, close: float, volume: float):
        self.ticker = ticker
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    # @property
    # def email(self):
    #     return f'{self.first}.{self.last}@email.com'
    #
    # @property
    # def fullname(self):
    #     return f'{self.first} {self.last}'
    #
    # def __repr__(self):
    #     return f'Employee("{self.first}", "{self.last}", "{self.pay}")'
