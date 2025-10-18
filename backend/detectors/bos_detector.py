import pandas as pd
from .swing_detector import find_swings

def detect_bos(df: pd.DataFrame, trend: str = 'uptrend'):
    swings = find_swings(df, left_bars=2, right_bars=2)
    df = pd.concat([df, swings], axis=1)
    swing_highs = df[df['is_swing_high']].index
    swing_lows = df[df['is_swing_low']].index

    if trend == 'downtrend' and len(swing_highs) >= 2:
        last_hh_idx = swing_highs[-1]
        last_hh_price = df.loc[last_hh_idx, 'high']
        after_hh = df.loc[last_hh_idx + pd.Timedelta(seconds=1):]
        if not after_hh.empty:
            bos_candidates = after_hh[after_hh['close'] < last_hh_price]
            if not bos_candidates.empty:
                first_bos = bos_candidates.iloc[0]
                return {
                    'type': 'bearish_bos',
                    'price': first_bos['close'],
                    'timestamp': first_bos.name,
                    'confirmed': first_bos['close'] < first_bos['open']
                }

    elif trend == 'uptrend' and len(swing_lows) >= 2:
        last_ll_idx = swing_lows[-1]
        last_ll_price = df.loc[last_ll_idx, 'low']
        after_ll = df.loc[last_ll_idx + pd.Timedelta(seconds=1):]
        if not after_ll.empty:
            bos_candidates = after_ll[after_ll['close'] > last_ll_price]
            if not bos_candidates.empty:
                first_bos = bos_candidates.iloc[0]
                return {
                    'type': 'bullish_bos',
                    'price': first_bos['close'],
                    'timestamp': first_bos.name,
                    'confirmed': first_bos['close'] > first_bos['open']
                }
    return None
