# Быстрый старт

## Что нужно знать

Этот проект состоит из **двух частей**:

1. **Backend** (папка `backend/`) - Python сервер, который:
   - Получает цены с Binance в реальном времени
   - Анализирует графики и генерирует торговые сигналы
   - Отправляет сигналы через WebSocket

2. **Telegram Mini App** (папка `telegram-mini-app/`) - React приложение, которое:
   - Показывает сигналы в красивом интерфейсе
   - Работает прямо в Telegram
   - Подключается к Backend через WebSocket

## Локальный запуск (для тестирования)

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Откройте http://localhost:8000/docs для проверки

### Telegram Mini App

```bash
cd telegram-mini-app
npm install
npm run dev
```

Откройте http://localhost:3000

## Деплой (публикация в интернет)

Читайте подробную инструкцию в файле `DEPLOY.md`

Краткая версия:

1. Загрузите код на GitHub
2. Создайте **Web Service** на Render.com для `backend/`
3. Создайте **Static Site** на Render.com для `telegram-mini-app/`
4. Настройте бота через @BotFather в Telegram
5. Готово!

## Что делает бот?

Бот анализирует 3 актива:
- **BTC/USD** (Bitcoin)
- **ETH/USD** (Ethereum)
- **EUR/USD** (Евро/Доллар)

Использует методы Smart Money Concepts:
- Break of Structure (BOS) - пробой структуры
- Order Blocks (OB) - зоны институционального интереса
- Технические индикаторы (RSI, MACD, EMA)

Когда находит хороший сигнал - отправляет в Telegram Mini App:
- Тип сделки (CALL/PUT)
- Зона входа
- Доходность
- RSI и другие индикаторы

## Нужна помощь?

Читайте:
- `README.md` - общая информация
- `DEPLOY.md` - подробная инструкция по деплою
- Или задайте вопрос в Issues на GitHub
