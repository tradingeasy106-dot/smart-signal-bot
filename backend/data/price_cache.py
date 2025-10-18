import pandas as pd
from collections import defaultdict, deque

class PriceCache:
    def __init__(self, max_bars=200):
        self.bars_m1 = defaultdict(lambda: deque(maxlen=max_bars))
        self.bars_h1 = defaultdict(lambda: deque(maxlen=100))

    def add_oanda_tick(self, symbol: str, bid: float, ask: float):
        price = (bid + ask) / 2
        now = pd.Timestamp.utcnow().floor('1min')
        key = (symbol, "mock")
        self._update_bar(self.bars_m1[key], now, price)
        self._update_h1_bar(self.bars_h1[key], now, price)

    def add_binance_kline(self, symbol: str, kline: dict):
        time = pd.to_datetime(kline["time"], unit='ms', utc=True).floor('1min')
        price_data = {'open': kline['open'], 'high': kline['high'], 'low': kline['low'], 'close': kline['close']}
        key = (symbol, "binance")
        self.bars_m1[key].append({'time': time, **price_data})
        self._update_h1_bar(self.bars_h1[key], time, kline['close'])

    def _update_bar(self, bars, time, price):
        if not bars or bars[-1]['time'] != time:
            bars.append({'time': time, 'open': price, 'high': price, 'low': price, 'close': price})
        else:
            last = bars[-1]
            last['high'] = max(last['high'], price)
            last['low'] = min(last['low'], price)
            last['close'] = price

    def _update_h1_bar(self, h1_bars, time, price):
        hour = time.floor('1h')
        if not h1_bars or h1_bars[-1]['time'] != hour:
            h1_bars.append({'time': hour, 'open': price, 'high': price, 'low': price, 'close': price})
        else:
            last = h1_bars[-1]
            last['high'] = max(last['high'], price)
            last['low'] = min(last['low'], price)
            last['close'] = price

    def get_dataframe(self, symbol: str, source: str, timeframe: str = 'M1') -> pd.DataFrame:
        key = (symbol, source)
        bars = self.bars_h1[key] if timeframe == 'H1' else self.bars_m1[key]
        if not bars:
            return pd.DataFrame()
        df = pd.DataFrame(list(bars))
        df.set_index('time', inplace=True)
        return df
