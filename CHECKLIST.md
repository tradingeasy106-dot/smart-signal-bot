# Чек-лист перед деплоем

## Backend файлы ✅

- [x] `backend/main.py` - FastAPI приложение
- [x] `backend/requirements.txt` - Python зависимости
- [x] `backend/.gitignore` - Игнорируемые файлы
- [x] `backend/data/__init__.py` - Пакет data
- [x] `backend/data/binance_client.py` - Binance WebSocket клиент
- [x] `backend/data/price_cache.py` - Кэш цен и свечей
- [x] `backend/detectors/__init__.py` - Пакет detectors
- [x] `backend/detectors/swing_detector.py` - Swing High/Low
- [x] `backend/detectors/bos_detector.py` - Break of Structure
- [x] `backend/detectors/ob_detector.py` - Order Blocks
- [x] `backend/detectors/ta_detector.py` - Технический анализ

## Telegram Mini App файлы ✅

- [x] `telegram-mini-app/package.json` - NPM зависимости
- [x] `telegram-mini-app/vite.config.ts` - Vite конфиг
- [x] `telegram-mini-app/tsconfig.json` - TypeScript конфиг
- [x] `telegram-mini-app/tsconfig.node.json` - TypeScript для Vite
- [x] `telegram-mini-app/index.html` - HTML шаблон
- [x] `telegram-mini-app/.env.example` - Пример env файла
- [x] `telegram-mini-app/.gitignore` - Игнорируемые файлы
- [x] `telegram-mini-app/src/main.tsx` - Точка входа
- [x] `telegram-mini-app/src/App.tsx` - Главный компонент

## Документация ✅

- [x] `README.md` - Основная документация
- [x] `DEPLOY.md` - Инструкция по деплою
- [x] `QUICK_START.md` - Быстрый старт
- [x] `CHECKLIST.md` - Этот чек-лист

## Функции Backend ✅

- [x] FastAPI приложение запускается
- [x] WebSocket endpoint `/ws`
- [x] CORS настроен для всех источников
- [x] Подключение к Binance WebSocket
- [x] Кэширование свечей M1 и H1
- [x] Генерация mock данных для EUR/USD
- [x] Детекция Break of Structure
- [x] Детекция Order Blocks
- [x] Технический анализ (RSI, MACD, EMA)
- [x] Генератор сигналов каждые 15 секунд
- [x] Broadcast сигналов всем клиентам

## Функции Frontend ✅

- [x] React приложение с TypeScript
- [x] WebSocket подключение к backend
- [x] Отображение статуса подключения
- [x] Список последних 5 сигналов
- [x] Цветовая индикация CALL/PUT
- [x] Отображение RSI с цветом
- [x] Адаптивный дизайн
- [x] Темная тема интерфейса

## Перед деплоем проверьте:

### Backend на Render.com
- [ ] Root Directory = `backend`
- [ ] Build Command = `pip install -r requirements.txt`
- [ ] Start Command = `python main.py`
- [ ] Runtime = Python 3
- [ ] Получен URL (например: https://xxx.onrender.com)

### Frontend на Render.com
- [ ] Root Directory = `telegram-mini-app`
- [ ] Build Command = `npm install && npm run build`
- [ ] Publish Directory = `dist`
- [ ] Environment Variable: `VITE_WS_URL` = `wss://xxx.onrender.com/ws`
- [ ] Получен URL (например: https://yyy.onrender.com)

### Telegram Bot
- [ ] Создан бот через @BotFather
- [ ] Создано Mini App через @BotFather
- [ ] Web App URL указан правильно
- [ ] Бот открывается в Telegram
- [ ] Mini App загружается
- [ ] WebSocket подключается
- [ ] Сигналы приходят

## Тестирование

### Локально (опционально)
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py
# Открыть http://localhost:8000/docs

# Frontend
cd telegram-mini-app
npm install
npm run dev
# Открыть http://localhost:3000
```

### На Render.com
1. Backend: `https://your-backend.onrender.com/docs`
2. Frontend: `https://your-frontend.onrender.com`
3. Telegram: Открыть бота и запустить Mini App

## Решение проблем

### Backend не запускается
- Проверьте логи в Render Dashboard
- Убедитесь, что все `.py` файлы на месте
- Проверьте `requirements.txt`

### WebSocket не подключается
- Используйте `wss://` (не `ws://`)
- Проверьте `VITE_WS_URL` в environment
- Проверьте CORS в `backend/main.py`

### Сигналы не приходят
- Подождите 30-60 секунд
- Проверьте логи backend
- Убедитесь, что Binance WebSocket работает

## Готово!

Если все пункты отмечены ✅ - ваш Smart Signal Bot готов к работе!
