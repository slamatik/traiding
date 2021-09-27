from bits import HorizontalBarChart

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# , engine='openpyxl'
def run():
    # Get Data from excel
    excel = pd.read_excel('BarLoader.xlsx', nrows=8, usecols=list(range(9)), na_filter=False, dtype={'date': datetime},
                          engine='openpyxl')
    excel = excel.replace(to_replace='\s+', value='', regex=True)
    excel = excel.replace({'plot_type': {'': 'b'},
                           'orientation': {'': 'h'},
                           'sorting': {'': None},
                           'y_axis': {'': 'l'}})
    # print(excel.columns[8::2])
    for idx, row in excel.iterrows():
        name = row.name
        fields = row.fields
        plot_type = row.plot_type
        orientation = row.orientation
        sorting = row.sorting
        y_axis = row.y_axis # todo
        date = row.date

        # Get list of tickers
        tickers = []
        for ticker_name in row[8::2]:
            if len(ticker_name) != 0:
                tickers.append(ticker_name)

        HorizontalBarChart()
        break


if __name__ == '__main__':
    run()
    # excel = pd.read_excel('BarLoader.xlsx', nrows=8, usecols=list(range(9)), na_filter=False, dtype={'date': datetime},
    #                       engine='openpyxl')
    # excel = excel.replace(to_replace='\s+', value='', regex=True)
    # excel = excel.replace({'plot_type': {'': 'b'},
    #                        'orientation': {'': 'h'},
    #                        'sorting': {'': None},
    #                        'y_axis': {'': 'l'}})
    # print(excel.sorting)
    # print(excel.y_axis)
