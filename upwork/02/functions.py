import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from xbbg import blp
from datetime import datetime

import yfinance as yf

# Graph Settings (can be moved to separate file if you want)
WIDTH = 0.35


def download_data(tickers, fields='PX_Last', start_date=datetime.today()):
    df = blp.bdh(tickers=tickers, flds=[fields], start_date=start_date)
    return df


def sort_data(data, sort_by, sort_type):
    # TODO
    pass


def plot_bar_chart(df, plot_type='', orientation='h', sort='', y_axis='l', date=datetime.today(), source='Bloomberg', plot=False):
    """
    Creates Bar Chart and saves it.
    :param df: pd.DataFrame, ticker data
    :param plot_type: str, '' - (empty string (default)) bar chart, 'c' - clustered, 's' - stacked TODO stacked
    :param orientation: str, 'h' - horizontal (default), 'v' - vertical
    :param sort: str, 'a' - ascending, 'd' - descending, '' - (empty string) no sorting
    :param y_axis: TODO find out what is it
    :param date: datetime, Date when df values were obtained (default - now)
    :param source: str, source of values (e.g. 'Bloomberg') TODO interfere with chart legend
    :param plot: bool, display graph after creation 
    :return: None
    """

    if plot:
        plt.show()


print(datetime.now().date())
