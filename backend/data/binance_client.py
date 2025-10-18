import asyncio
import websockets
import json

class BinanceClient:
    async def stream_klines(self, symbols: list, interval: str, callback):
        streams = "/".join([f"{s.lower()}@kline_{interval}" for s in symbols])
        url = f"wss://stream.binance.com:9443/ws/{streams}"
        async with websockets.connect(url) as ws:
            async for message in ws:
                data = json.loads(message)
                if data.get("e") == "kline":
                    kline = data["k"]
                    await callback({
                        "symbol": data["s"],
                        "time": int(kline["t"]),
                        "open": float(kline["o"]),
                        "high": float(kline["h"]),
                        "low": float(kline["l"]),
                        "close": float(kline["c"]),
                        "volume": float(kline["v"])
                    })
