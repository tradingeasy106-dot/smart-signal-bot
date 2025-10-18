# Smart Signal Bot

Торговый бот для генерации сигналов на бинарных опционах с использованием Smart Money Concepts и технического анализа.

## Структура проекта

```
smart-signal-bot/
├── backend/                 # FastAPI бэкенд
│   ├── main.py             # Главный файл приложения
│   ├── requirements.txt    # Python зависимости
│   ├── data/               # Модули для работы с данными
│   │   ├── __init__.py
│   │   ├── binance_client.py    # Клиент Binance WebSocket
│   │   └── price_cache.py       # Кэш цен и таймфреймов
│   └── detectors/          # Детекторы торговых сигналов
│       ├── __init__.py
│       ├── bos_detector.py      # Break of Structure
│       ├── ob_detector.py       # Order Blocks
│       ├── swing_detector.py    # Swing High/Low
│       └── ta_detector.py       # Технический анализ (RSI, MACD, EMA)
└── telegram-mini-app/      # Telegram Mini App (React)
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── main.tsx
        └── App.tsx         # Интерфейс приложения
```

## Установка и запуск

### Backend (Python FastAPI)

1. Перейдите в папку backend:
```bash
cd backend
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервер:
```bash
python main.py
```

Сервер запустится на `http://localhost:8000`

### Telegram Mini App (React)

1. Перейдите в папку telegram-mini-app:
```bash
cd telegram-mini-app
```

2. Установите зависимости:
```bash
npm install
```

3. Создайте файл `.env`:
```bash
cp .env.example .env
```

4. Отредактируйте `.env` и укажите URL вашего бэкенда:
```
VITE_WS_URL=ws://localhost:8000/ws
```

5. Запустите приложение:
```bash
npm run dev
```

## Деплой на Render.com

### Backend

1. Создайте новый Web Service на Render.com
2. Подключите ваш GitHub репозиторий
3. Настройте:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python main.py`
   - **Environment**: Python 3

4. После деплоя скопируйте URL вашего сервиса (например, `https://your-app.onrender.com`)

### Telegram Mini App

1. Создайте новый Static Site на Render.com
2. Настройте:
   - **Build Command**: `cd telegram-mini-app && npm install && npm run build`
   - **Publish Directory**: `telegram-mini-app/dist`

3. Добавьте переменную окружения:
   - **VITE_WS_URL**: `wss://your-backend-app.onrender.com/ws`

## Подключение к Telegram

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Настройте Mini App командой `/newapp`
4. Укажите URL вашего Telegram Mini App с Render.com

## Особенности

- Real-time анализ цен с Binance через WebSocket
- Детекция Break of Structure (BOS)
- Определение Order Blocks (OB)
- Подтверждение через RSI, MACD, EMA
- WebSocket связь между бэкендом и клиентом
- Красивый интерфейс с индикацией статуса подключения

## Торгуемые активы

- BTC/USD (Binance: BTCUSDT)
- ETH/USD (Binance: ETHUSDT)
- EUR/USD (Mock data)

## Лицензия

MIT
