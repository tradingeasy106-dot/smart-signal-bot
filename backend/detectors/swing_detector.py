import pandas as pd

def find_swings(df: pd.DataFrame, left_bars: int = 2, right_bars: int = 2):
    highs = df['high'].values
    lows = df['low'].values
    n = len(df)
    is_swing_high = [False] * n
    is_swing_low = [False] * n

    for i in range(left_bars, n - right_bars):
        if (highs[i] > max(highs[i - left_bars:i]) and
            highs[i] > max(highs[i + 1:i + right_bars + 1])):
            is_swing_high[i] = True
        if (lows[i] < min(lows[i - left_bars:i]) and
            lows[i] < min(lows[i + 1:i + right_bars + 1])):
            is_swing_low[i] = True

    return pd.DataFrame({
        'is_swing_high': is_swing_high,
        'is_swing_low': is_swing_low
    }, index=df.index)
