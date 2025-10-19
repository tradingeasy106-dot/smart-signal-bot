# backend/data/cryptocompare_client.py
import asyncio
import requests
import time
from datetime import datetime, timezone

class CryptoCompareClient:
    def __init__(self):
        self.base_url = "https://min-api.cryptocompare.com/data"
        self.last_request = 0
        self.request_delay = 0.2  # Безопасная задержка между запросами

    async def fetch_minute_candle(self, fsym: str, tsym: str = "USD"):
        """Получает последнюю M1-свечу для криптовалюты"""
        now = time.time()
        if now - self.last_request < self.request_delay:
            await asyncio.sleep(self.request_delay - (now - self.last_request))
        
        url = f"{self.base_url}/v2/histominute"
        params = {
            "fsym": fsym,
            "tsym": tsym,
            "limit": 1,
            "toTs": int(datetime.now(timezone.utc).timestamp())
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if data.get("Response") == "Success" and data.get("Data"):
                candle = data["Data"]["Data"][-1]
                return {
                    "symbol": f"{fsym}/USD",
                    "time": candle["time"],
                    "open": candle["open"],
                    "high": candle["high"],
                    "low": candle["low"],
                    "close": candle["close"],
                    "volume": candle["volumefrom"]
                }
        except Exception as e:
            print(f"❌ Ошибка CryptoCompare для {fsym}: {e}")
            return None
        
        self.last_request = time.time()
        return None

    async def stream_klines(self, symbols: list, callback):
        """Эмулирует поток данных: опрашивает каждую минуту"""
        print(f"✅ Запущен CryptoCompare для: {symbols}")
        while True:
            for fsym in symbols:
                kline = await self.fetch_minute_candle(fsym, "USD")
                if kline:
                    await callback(kline)
            await asyncio.sleep(60)  # Обновление раз в минуту