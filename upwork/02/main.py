from bits import HorizontalBarChart

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def run():
    excel = pd.read_excel('BarLoader.xlsx', nrows=8, na_filter=False, dtype={'date':datetime})
    # print(excel.columns[8::2])
    for idx, row in excel.iterrows():
        # Fields
        fields = row.field

        # Plot type
        plot_type = row.plot_type
        if len(plot_type) == 0:
            plot_type = 'b'

        # Orientation
        if len(plot_type) == 0:
            orientation = 'h'

        # Sorting


        # y_axis todo at the end


        # Get list of tickers
        tickers = []
        for ticker_name in row[8::2]:
            if len(ticker_name) != 0:
                tickers.append(ticker_name)
        break


if __name__ == '__main__':
    # run()
    excel = pd.read_excel('BarLoader.xlsx', nrows=8, usecols=list(range(9)), na_filter=False, dtype={'date':datetime})
    excel = excel.replace(to_replace='\s+', value='', regex=True)
    excel = excel.replace({'plot_type': {'': 'b'}, 'orientation': {'': 'h'}, 'sorting': {'': None}, 'y_axis': {'': 'l'}})
    print(excel.sorting)
    print(excel.y_axis)
