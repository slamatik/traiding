# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 00:21:30 2020

@author: mark
"""
import pickle as p
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import talib
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
from xbbg import blp

# Get today's date as UTC timestamp
today = datetime.today().strftime("%d/%m/%Y")
today = datetime.strptime(today + " +0000", "%d/%m/%Y %z")
to = int(today.timestamp())
# Get date ten years ago as UTC timestamp
ten_yr_ago = today - relativedelta(years=10)
fro = int(ten_yr_ago.timestamp())

ticker = 'DAX Index'
start_date = '2015-07-01'
end_date = '2020-10-31'


def get_price_hist(ticker):
    # start_date = start_date
    # end_date = end_date
    # Put stock price data in dataframe
    # Put stock price data in dataframe
    data = blp.bdh(tickers=ticker, flds=['PX_Open', 'PX_High', 'PX_Low', 'Last_price', 'PX_Volume'],
                   start_date=start_date, end_date=end_date)
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    data.to_pickle('pandas from feed after api blp request.p')
    return data


ticker = ticker
nflx_df = get_price_hist(ticker)


def get_indicators(data):
    # Get MACD
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])

    # Get MA10 and MA30
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)

    # Get RSI
    data["rsi"] = talib.RSI(data["Close"])
    return data


nflx_df2 = get_indicators(nflx_df)

plt.plot(nflx_df)
# determining the name of the file 
file_name = 'example2.xlsx'

# saving the excel 
nflx_df.to_excel(file_name)
print('DataFrame is written to Excel File example 2 successfully.')


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
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=0.8)
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
    plt.savefig("C:/Users/marc/Documents/Python Scripts/charts/" + ticker + ".png", bbox_inches="tight")

    plt.show()


plot_chart(nflx_df2, 40000, ticker)
plt.close()
