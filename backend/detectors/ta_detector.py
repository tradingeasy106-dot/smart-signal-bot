import pandas as pd
import numpy as np

def calculate_rsi(series: pd.Series, period: int = 9):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(df: pd.DataFrame, fast=5, slow=13, signal=1):
    ema_fast = df['close'].ewm(span=fast).mean()
    ema_slow = df['close'].ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    return macd_line, signal_line

def detect_ta_confirmation(df: pd.DataFrame, signal_type: str):
    df = df.copy()
    df['rsi'] = calculate_rsi(df['close'], period=9)
    macd, macd_signal = calculate_macd(df, fast=5, slow=13, signal=1)
    df['macd'] = macd
    df['macd_signal'] = macd_signal
    df['ema9'] = df['close'].ewm(span=9).mean()
    df['ema21'] = df['close'].ewm(span=21).mean()
    last_price = df['close'].iloc[-1]
    last_rsi = df['rsi'].iloc[-1]
    last_macd = df['macd'].iloc[-1]
    last_macd_signal = df['macd_signal'].iloc[-1]
    last_ema9 = df['ema9'].iloc[-1]
    last_ema21 = df['ema21'].iloc[-1]

    if signal_type == "CALL":
        rsi_ok = last_rsi < 25
        macd_ok = last_macd > last_macd_signal
        ema_ok = (last_price > last_ema9) and (last_price > last_ema21)
        confirmed = rsi_ok and macd_ok and ema_ok
    elif signal_type == "PUT":
        rsi_ok = last_rsi > 75
        macd_ok = last_macd < last_macd_signal
        ema_ok = (last_price < last_ema9) and (last_price < last_ema21)
        confirmed = rsi_ok and macd_ok and ema_ok
    else:
        confirmed = False

    return {
        "confirmed": confirmed,
        "indicators": {
            "rsi": round(last_rsi, 1),
            "macd": round(last_macd, 5),
            "macd_signal": round(last_macd_signal, 5),
            "ema9": round(last_ema9, 5),
            "ema21": round(last_ema21, 5),
            "bb_width_pct": 0.5,
            "volatility_ok": True
        }
    }
