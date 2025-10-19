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
def add_binance_kline(self, symbol: str, kline: dict):
    time = pd.to_datetime(kline["time"], unit='s', utc=True).floor('1min')
    price_data = {
        'open': kline['open'],
        'high': kline['high'],
        'low': kline['low'],
        'close': kline['close']
    }
    key = (symbol, "cryptocompare")
    self.bars_m1[key].append({'time': time, **price_data})
    self._update_h1_bar(self.bars_h1[key], time, kline['close'])