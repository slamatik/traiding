import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from xbbg import blp

source = 'Bloomberg'

class BarChart:
    def __init__(self, df: pd.DataFrame, y_axis=None):
        self.df = df
        self.n_rows = len(self.df)  # number of tickers
        self.n_cols = len(self.df.columns)  # number of fields

        self.labels = df.index  # list of ticker names

        # self.size = round(1 / self.n_cols - 0.1, 2)
        self.size = round(1 / self.n_cols, 2)  # size of a single bar
        self.gap = self.size * 2  # gap between groups

        self.x = np.zeros(self.n_rows)  # initialize empty list for bar groups position
        for i in range(self.n_rows):
            self.x[i] = (round((self.size * self.n_cols + self.gap) * i, 2))

        self.label_position = self.x + (self.size * self.n_cols) / 2  # x label positions (middle of the bar(s))

        self.fig, self.ax = plt.subplots(figsize=(12, 8)) # initialize matplotlib figure
        plt.figtext(0.86, 0.02, f'Source: {source} Date: {datetime.today().date().strftime("%d/%m/%Y")}',
                    ha='center',
                    fontsize=6)

        # Figure borders
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        if y_axis == 'r': self.ax.tick_params(labelright=True, right=True, labelleft=False, left=False)
        if y_axis == 'b': self.ax.tick_params(labelright=True, right=True)


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
    def __init__(self, df, y_axis=None, sort=False):
        super().__init__(df, y_axis)
        if sort: self.sort_data(sort)
        for col in range(self.n_cols):
            ax.barh(self.x + self.size * col, df[df.columns[col]], height=self.size, label=df.columns[col])
        plt.yticks(self.x, df.index)
        ax.legend()
        plt.show()


class VerticalBarChart(BarChart):
    def __init__(self, df, y_axis=None, sort=None):
        super().__init__(df, y_axis)
        if sort: self.sort_data(sort)
        plt.grid(b=True, which='major', axis='y', color='grey', alpha=.5)
        for col in range(self.n_cols):
            self.ax.bar(self.x + self.size * col, df[df.columns[col]], width=self.size, label=df.columns[col])

        plt.xticks(self.label_position, df.index)
        self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False)
        plt.show()


def get_data():
    with open('yf_data.pkl', 'rb') as f:
        df = pickle.load(f)
        tickers = ['msft', 'tsla', 'aapl', 'nio', 'pltr', 'adsk', 'clf']
        fields = ['operatingMargins', 'revenueGrowth', 'currentRatio', 'quickRatio']

        yf_dict = {i: [] for i in tickers}
        for i in range(len(tickers)):
            yf_dict[tickers[i]].append(df[tickers[i]]['operatingMargins'])
            # yf_dict[tickers[i]].append(df[tickers[i]]['revenueGrowth'])
            # yf_dict[tickers[i]].append(df[tickers[i]]['currentRatio'])
            # yf_dict[tickers[i]].append(df[tickers[i]]['quickRatio'])

        yf_df = pd.DataFrame(yf_dict, index=[fields[0]]).T
        print(yf_df.columns)
    # return
    return yf_df


def get_data2():
    with open('example.pkl', 'rb') as f:
        df = pickle.load(f)

    # return df.drop('current_trr_ytd', axis=1)
    return df


if __name__ == '__main__':
    df = get_data2()
    VerticalBarChart(df)
