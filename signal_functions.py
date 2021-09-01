import pandas as pd


def is_bearish_candlestick(candle):
    return candle.Close < candle.Open


def is_bullish_candlestick(candle):
    return candle.Close > candle.Open


def bullish_engulfing(today_idx, df):
    today = df.iloc[today_idx]
    today_1 = df.iloc[today_idx - 1]
    if is_bearish_candlestick(today_1) and today.Open < today_1.Close and today.Close > today_1.Open:
        return True
    return False


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


def hammer(today_idx, df):
    today = df.iloc[today_idx]
    today_1 = df.iloc[today_idx - 1]
    today_2 = df.iloc[today_idx - 2]
    if is_bullish_candlestick(today) and is_bullish_candlestick(today_1) and is_bearish_candlestick(today_2):
        if today_1.Close < today.Open and today_1.Close < today_2.Close and today_1.Close == today_1.High:
            body_length = today_1.Close - today_1.Open
            wick_length = today_1.Open - today_1.Low
            if wick_length > 2 * body_length:
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
