import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from xbbg import blp

plt.style.use('Solarize_Light2')


# plt.style.use('seaborn-whitegrid')


class BarChart:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.n_rows = len(self.df)
        self.n_cols = len(self.df.columns)
        self.size = 1 / self.n_cols - 0.1
        self.x = np.arange(self.n_rows)

    def sort_data(self, sort_type):
        """
        Sorts by column index or name
        :param sort_by: str/int
        :param sort_type: str - Ascending/Descending
        :return: None
        """

        sort_by = self.df.columns[0]
        ascending = True
        if sort_type == 'd':
            ascending = False

        self.df.sort_values(by=sort_by, axis=0, inplace=True, ascending=ascending)


class HorizontalBarChart(BarChart):
    def __init__(self, df, sort=False):
        super().__init__(df)
        if sort:
            self.sort_data(sort)
        fig, ax = plt.subplots(figsize=(12, 8))
        for col in range(self.n_cols):
            ax.barh(self.x + self.size * col, df[df.columns[col]], height=self.size, label=df.columns[col])
        plt.yticks(self.x, df.index)
        ax.legend()
        plt.show()


class VerticalBarChart(BarChart):
    def __init__(self, df, sort=False):
        super().__init__(df)
        if sort:
            self.sort_data(sort)
        fig, ax = plt.subplots(figsize=(12, 8))
        for col in range(self.n_cols):
            ax.bar(self.x + self.size * col, df[df.columns[col]], width=self.size, label=df.columns[col])
        plt.xticks(self.x, df.index)
        ax.legend()
        plt.show()


def gen_yf_data():
    with open('yf_data.pkl', 'rb') as f:
        yf_data = pickle.load(f)

    yf_tickers = ['msft', 'tsla', 'aapl', 'nio', 'pltr', 'adsk', 'clf']
    yf_dict = {i: [] for i in yf_tickers}
    for ticker in yf_tickers:
        yf_dict[ticker].append(yf_data[ticker]['operatingMargins'])
        yf_dict[ticker].append(yf_data[ticker]['revenueGrowth'])
        yf_dict[ticker].append(yf_data[ticker]['currentRatio'])
    yf_df = pd.DataFrame(yf_dict, index=['operatingMargins', 'revenueGrowth', 'currentRatio']).T
    return yf_df


def download_data(tickers, fields, start_date=datetime.today()):
    # temporary data
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
    data = data['bdp_mm']

    # actual todo
    # df = blp.bdp(tickers=tickers, flds=fields)

    # df = blp.bdh()
    # df = blp.bds()

    return data


# data = gen_yf_data()
# HorizontalBarChart(data)

if __name__ == '__main__':
    print('kek')
