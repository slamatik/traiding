import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from xbbg import blp
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import yfinance as yf

legend_size = 10
axes_size = 10
plt.rc('xtick', labelsize=axes_size)
plt.rc('ytick', labelsize=axes_size)
plt.rc('legend', fontsize=legend_size)
plt.rc('axes', labelsize=50)
plt.rcParams['timezone'] = 'GMT'


def get_price_hist(ticker, start_date, end_date):
    """
    Creates OHLCV DataFrame
    :param ticker: str
    :param start_date: start_date
    :param end_date: end_date, default today
    :return: pd.DataFrame
    """
    data = yf.download(ticker, start=start_date, end_date=end_date)
    # data = blp.bdh(tickers=ticker, flds=['PX_Open', 'PX_High', 'PX_Low', 'Last_price', 'PX_Volume'],
    #                start_date=start_date, end_date=end_date)
    # data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    # data.to_pickle('pandas from feed after api blp request.p')
    return data


def get_date(your_input):
    """
    Calculates date days/months/years ago
    :param your_input: example: 12D, 3M, 5Y, YTD
    :return: new date 'YYYY-MM-DD'
    """
    your_input = your_input.lower()
    if your_input[-1] not in ['d', 'm', 'y']:
        raise ValueError('Wrong input for date, please use D/M/Y/YTD')
    today = datetime.now()
    if your_input == 'ytd':
        return date(today.year, 1, 1)
    number = int(your_input[:-1])
    if your_input[-1] == 'd':
        result = today - relativedelta(days=number)
    if your_input[-1] == 'm':
        result = today - relativedelta(months=number)
    if your_input[-1] == 'y':
        result = today - relativedelta(years=number)
    return result.date()


def get_indicators(data):
    """
    Updates DataFrame with indicators
    :param data: pd.DataFrame
    :return: pd.DataFrame
    """
    data["macd"], data["macd_signal"], data["macd_hist"] = ta.MACD(data['Close'])

    # Get MA10 and MA30
    data["ma10"] = ta.MA(data["Close"], timeperiod=10)
    data["ma30"] = ta.MA(data["Close"], timeperiod=30)

    # Get RSI
    data["rsi"] = ta.RSI(data["Close"])
    return data


def plot_chart(data, ticker, n=0, plot=False):
    """
    Saves chart in the background
    :param plot: bool: Whether to plot chart after chart been created
    :param data: : pd.DateFrame: OHLCV DataFrame
    :param ticker: str: name of the ticker
    :param n: int: last number of days
    :return: None
    """
    # To change color you can update argument "c" or "color" in the plot function bellow
    # You can find simple colors supported by matplotlib here https://matplotlib.org/stable/gallery/color/named_colors.html

    # controlls width of lines by default is 1. This will change all LINES on the plot.
    line_w = 2

    # Filter number of observations to plot
    data = data.iloc[-n:]

    # Create figure and set axes for subplots
    fig = plt.figure()
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
    ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
    ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
    ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)

    # Get nested list of date, open, high, low and close prices
    ohlc = []
    for idx, row in data.iterrows():
        openp, highp, lowp, closep = row[:4]
        ohlc.append([date2num(idx), openp, highp, lowp, closep])

    # Format x-axis ticks as dates
    ax_candle.xaxis_date()

    # Limits x-axis (removes the gap)
    ax_candle.set_xlim(xmin=ohlc[0][0], xmax=ohlc[-1][0])

    # Plot candlestick chart
    # you can set linewidth to a different number if you dont want all of them to be specific size
    # ex: linewidth=3, this can be set separately to all plot functions bellow
    ax_candle.plot(data.index, data["ma10"], label="MA10", linewidth=line_w, c='yellow')
    ax_candle.plot(data.index, data["ma30"], label="MA30", linewidth=line_w, c='cyan')

    # width controls width of the candle, colorup is a color of bull candle, colordown color of red candle
    candlestick_ohlc(ax_candle, ohlc, colorup="b", colordown="r", width=0.8)
    ax_candle.legend()

    # Plot MACD
    ax_macd.plot(data.index, data["macd"], label="macd", linewidth=line_w, c='blue')
    ax_macd.plot(data.index, data["macd_signal"], label="signal", linewidth=line_w, c='orange')
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist", color='slategrey')
    ax_macd.legend()

    # Plot RSI
    # Above 70% = overbought, below 30% = oversold
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought", c='red')
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold", c='green')
    ax_rsi.plot(data.index, data["rsi"], label="rsi", linewidth=line_w, c='black')
    ax_rsi.legend()

    # Show volume in millions
    ax_vol.bar(data.index, data["Volume"] / 1000000, color='coral')
    ax_vol.set_ylabel("(Million)")

    # Save the chart as PNG
    # Change path here if needed, remove "transparent=True" if needed
    fig.savefig(ticker + ".png", bbox_inches="tight", transparent=False)

    if plot:
        plt.show()


def run():
    today = date.today()
    # reads excel file (must be in the same folder as this file)
    excel = pd.read_excel('inputbb.xlsx', na_filter=False)
    for idx, row in excel.iterrows():
        ticker = row.Ticker
        start_date = row['Start Date']
        end_date = row['End Date']
        # star_date
        # checks if cell is empty
        if len(start_date) == 0:
            start_date = today - relativedelta(years=1)
        # else there is something
        else:
            # long input? DD.MM.YYYY
            if len(start_date) > 6:
                start_date = datetime.strptime(start_date, '%d.%m.%Y')
            else:
                # Smaller input like 60D, 3M
                start_date = get_date(start_date)
        download_date = start_date - relativedelta(years=1)

        # end_date
        # checks if cell is empty
        if len(end_date) == 0:
            end_date = today
        # else there is something
        else:
            # long input? DD.MM.YYYY
            if len(end_date) > 6:
                end_date = datetime.strptime(end_date, '%d.%m.%Y')
            else:
                # Smaller input like 60D, 3M
                end_date = get_date(start_date)


        df = get_price_hist(ticker, download_date, end_date)
        df = get_indicators(df)
        # run plot_chart(data, ticker, plot=True) if you want to see plots (they still will be saved)
        plot_chart(df.loc[start_date:], ticker, plot=True)
        break


if __name__ == '__main__':
    run()
