import pandas as pd


def is_bearish_candlestick(candle):
    return candle.Close < candle.Open


def is_bullish_candlestick(candle):
    return candle.Close > candle.Open


def below_ema(row):
    return row.Close < row.ema50


def bullish_engulfing(df, today_idx):
    today = df.iloc[today_idx]
    today_1 = df.iloc[today_idx - 1]
    if is_bearish_candlestick(today_1) and today.Open < today_1.Close and today.Close > today_1.Open:
        return True
    return False


def hammer(df, today_idx):
    today = df.iloc[today_idx]
    if below_ema(today):
        if is_bullish_candlestick(today):
            body = today.Close - today.Open
            bottom_wick = today.Open - today.Low
            upper_wick = today.High - today.Close
            if bottom_wick > 2 * body and upper_wick < body:
                return True
        elif is_bearish_candlestick(today):
            body = today.Open - today.Close
            bottom_wick = today.Close - today.Low
            upper_wick = today.High - today.Open
            if bottom_wick > 2 * body and upper_wick < body:
                return True
    return False


def inverse_hammer(df, today_idx):
    today = df.iloc[today_idx]
    if below_ema(today):
        if is_bullish_candlestick(today):
            body = today.Close - today.Open
            bottom_wick = today.Open - today.Low
            upper_wick = today.High - today.Close
            if upper_wick > 2 * body and bottom_wick < body:
                return True


def three_white_soldiers(today_idx, df):
    today = df.iloc[today_idx]
    today_1 = df.iloc[today_idx - 1]
    today_2 = df.iloc[today_idx - 2]
    if is_bullish_candlestick(today) and is_bullish_candlestick(today_1) and is_bullish_candlestick(today_2):
        if today_1.Open < today.Open < today_1.Close < today.Close and \
                today_2.Open < today_1.Open < today_2.Close < today_1.Close:
            return True
    return False


def three_line_strike(today, today_1, today_2, today_3):
    if is_bearish_candlestick(today) and three_white_soldiers(today_1, today_2, today_3):
        if today.Open > today_1.Close and today.Close < today_3.Open:
            return True
    return False


def three_outside_up(today, today_1, today_2):
    if is_bullish_engulfing(today_1, today_2) and today.Close > today_1.Close:
        return True
    return False


def piercing_line(today_idx, df):
    today = df.iloc[today_idx]
    today_1 = df.iloc[today_idx - 1]
    if is_bearish_candlestick(today_1) and is_bullish_candlestick(today):
        if today.Open < today_1.Close and today.Close < today_1.Open:
            middle = today_1.Open - today_1.Close
            if today.Close > middle:
                return True
    return False


def is_consolidating(df, pct=2):
    recent_candlesticks = df[-15:]
    max_close = recent_candlesticks.Close.max()
    min_close = recent_candlesticks.Close.min()

    threshold = 1 - pct / 100
    if min_close > (max_close * threshold):
        return True


def is_breaking_out(df, pct=2):
    last_close = df[-1:].Close.values[0]

    if is_consolidating(df[:-1], pct):
        recent_closes = df[-16: -1]

        if last_close > recent_closes.Close.max():
            return True
