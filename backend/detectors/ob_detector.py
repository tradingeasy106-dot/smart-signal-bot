import pandas as pd
import numpy as np

def detect_order_blocks(df: pd.DataFrame, lookback_bars: int = 50):
    df = df.copy()
    df['body'] = abs(df['close'] - df['open'])
    df['tr'] = np.maximum(df['high'] - df['low'],
                         np.maximum(np.abs(df['high'] - df['close'].shift(1)),
                                   np.abs(df['low'] - df['close'].shift(1))))
    df['atr'] = df['tr'].rolling(window=14).mean()
    ob_list = []
    n = len(df)

    for i in range(2, min(lookback_bars, n)):
        current = df.iloc[i]
        prev = df.iloc[i - 1]
        if current['atr'] > 0 and current['body'] > 2 * current['atr']:
            ob_low = min(prev['open'], prev['close'])
            ob_high = max(prev['open'], prev['close'])
            ob_type = 'bullish_ob' if current['close'] > current['open'] else 'bearish_ob'
            future = df.iloc[i + 1:]
            tested = False
            if not future.empty:
                tested = ((future['low'] <= ob_high) & (future['high'] >= ob_low)).any()
            if not tested:
                ob_list.append({
                    'type': ob_type,
                    'zone_low': ob_low,
                    'zone_high': ob_high,
                    'timestamp': prev.name,
                    'tested': tested
                })
    return ob_list
