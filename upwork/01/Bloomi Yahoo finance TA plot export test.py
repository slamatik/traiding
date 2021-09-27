# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 00:21:30 2020

@author: mark
"""

import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import talib
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import openpyxl
from pathlib import Path
from xbbg import blp


def get_price_hist(arr):
    ticker = arr[0]
    start_date = arr[1]
    end_date = arr[2]

    # Get today's date as UTC timestamp
    if end_date == None:
        today = datetime.today().strftime("%d/%m/%Y")
        today = datetime.strptime(today + " +0000", "%d/%m/%Y %z")
        end_date = int(today.timestamp())
    # Get date ten years ago as UTC timestamp
    if start_date == None:
        if type(end_date) != int:
            ten_yr_ago = end_date - relativedelta(years=10)
        else:
            ten_yr_ago = datetime.fromtimestamp(end_date) - relativedelta(years=10)
        start_date = int(ten_yr_ago.timestamp())

    if type(start_date) != int:
        # start_date = '2019-07-01'
        # start_date = datetime.strptime(start_date, "%yyyy/%mm/%dd")   
        start_date = datetime.fromisoformat(start_date)
        start_date = start_date.strftime("%d/%m/%Y")
        start_date = datetime.strptime(start_date + " +0000", "%d/%m/%Y %z")
        start_date = int(start_date.timestamp())
        # type(start_date)
        # print(type(datetime.today()))

    if type(end_date) != int:
        # end_date = '2020-10-31'
        # end_date = datetime.strptime(end_date, "%yyyy/%mm/%dd")
        end_date = datetime.fromisoformat(end_date)
        end_date = end_date.strftime("%d/%m/%Y")
        end_date = datetime.strptime(end_date + " +0000", "%d/%m/%Y %z")
        end_date = int(end_date.timestamp())
        # end_date

    # Put stock price data in dataframe
    # Put stock price data in dataframe

    # url = "https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={fro}&period2={to}&interval=1d&events=history".format(ticker=ticker, fro=start_date, to=end_date)
    # data = pd.read_csv(url)

    data = blp.bdh(tickers=ticker, flds=['PX_Open', 'PX_High', 'PX_Low', 'Last_price', 'PX_Volume'],
                   start_date=start_date, end_date=end_date)
    # data.columns = ['Open','High','Low','Close','Volume']
    data.columns.set_levels(['Open', 'High', 'Low', 'Close', 'Volume'], level=1, inplace=True)

    data.index = data["Date"].apply(lambda x: pd.Timestamp(x))
    data.drop("Date", axis=1, inplace=True)

    print(data)

    return data


def get_indicators(data):
    # Get MACD
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])

    # Get MA10 and MA30
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)

    # Get RSI
    data["rsi"] = talib.RSI(data["Close"])
    return data


def plot_chart(data, n, ticker):
    # Filter number of observations to plot
    data = data.iloc[-n:]

    # Create figure and set axes for subplots
    fig = plt.figure()
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
    ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
    ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
    ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)

    # Format x-axis ticks as dates
    ax_candle.xaxis_date()

    # Get nested list of date, open, high, low and close prices
    ohlc = []
    for date, row in data.iterrows():
        openp, highp, lowp, closep = row[:4]
        ohlc.append([date2num(date), openp, highp, lowp, closep])

    # Plot candlestick chart
    ax_candle.plot(data.index, data["ma10"], label="MA10")
    ax_candle.plot(data.index, data["ma30"], label="MA30")
    candlestick_ohlc(ax_candle, ohlc, colorup="b", colordown="r", width=0.8)
    ax_candle.legend()

    # Plot MACD
    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.legend()

    # Plot RSI
    # Above 70% = overbought, below 30% = oversold
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
    ax_rsi.plot(data.index, data["rsi"], label="rsi")
    ax_rsi.legend()

    # Show volume in millions
    ax_vol.bar(data.index, data["Volume"] / 1000000)
    ax_vol.set_ylabel("(Million)")

    # Save the chart as PNG
    fig.savefig("charts/" + ticker + ".png", bbox_inches="tight")

    plt.show()


xlsx_file = Path('inputbb_old.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
# Read the active sheet:
sheet = wb_obj.active
data = sheet.values
columns = next(data)[0:]

df = pd.DataFrame(data, columns=columns)

toSend = []
for d in df.values:
    toSend.append([d[0].split(" ")[0], d[2], d[3]])
# toSend

for datas in toSend:
    nflx_df = get_price_hist(datas)
    nflx_df2 = get_indicators(nflx_df)
    plot_chart(nflx_df2, 180, datas[0])
