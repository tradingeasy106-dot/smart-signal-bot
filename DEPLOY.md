# Инструкция по деплою на Render.com

## Шаг 1: Подготовка репозитория GitHub

1. Создайте новый репозиторий на GitHub
2. Загрузите туда папки `backend` и `telegram-mini-app` из этого проекта
3. Убедитесь, что структура выглядит так:

```
your-repo/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── data/
│   └── detectors/
└── telegram-mini-app/
    ├── package.json
    ├── vite.config.ts
    └── src/
```

## Шаг 2: Деплой Backend на Render.com

### 2.1. Создайте новый Web Service

1. Зайдите на [render.com](https://render.com) и нажмите **New → Web Service**
2. Подключите ваш GitHub репозиторий
3. Выберите репозиторий из списка

### 2.2. Настройте Web Service

Заполните следующие поля:

- **Name**: `smart-signal-backend` (или любое другое имя)
- **Region**: Выберите ближайший регион
- **Branch**: `main` (или `master`)
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Plan**: Free (или платный по желанию)

### 2.3. Добавьте переменные окружения (опционально)

В разделе **Environment** можете добавить:

- `PORT` = `8000` (автоматически устанавливается Render)

### 2.4. Деплой

1. Нажмите **Create Web Service**
2. Дождитесь завершения билда (3-5 минут)
3. После успешного деплоя вы получите URL вида:
   ```
   https://smart-signal-backend.onrender.com
   ```
4. **ВАЖНО**: Скопируйте этот URL! Он понадобится для Mini App

## Шаг 3: Деплой Telegram Mini App на Render.com

### 3.1. Создайте новый Static Site

1. Нажмите **New → Static Site**
2. Выберите тот же репозиторий

### 3.2. Настройте Static Site

Заполните:

- **Name**: `smart-signal-app`
- **Branch**: `main`
- **Root Directory**: `telegram-mini-app`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`

### 3.3. Добавьте переменную окружения

В разделе **Environment**:

- **Key**: `VITE_WS_URL`
- **Value**: `wss://smart-signal-backend.onrender.com/ws`

  (замените на ваш URL из Шага 2)

### 3.4. Деплой

1. Нажмите **Create Static Site**
2. Дождитесь билда (2-3 минуты)
3. После деплоя вы получите URL:
   ```
   https://smart-signal-app.onrender.com
   ```

## Шаг 4: Настройка Telegram Bot

### 4.1. Создайте бота через BotFather

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Введите название бота: `SmartSignal Pro`
4. Введите username: `smartsignal_pro_bot` (или свой)
5. Сохраните токен бота!

### 4.2. Создайте Mini App

1. В BotFather отправьте `/newapp`
2. Выберите вашего бота
3. Введите название: `SmartSignal Pro`
4. Введите описание: `Trading signals based on Smart Money Concepts`
5. Загрузите иконку (512x512 PNG)
6. **Web App URL**: `https://smart-signal-app.onrender.com`
7. Введите короткое название: `smartsignal`

### 4.3. Готово!

Ваш бот готов! Откройте его в Telegram и нажмите кнопку меню для запуска Mini App.

## Проверка работы

### Backend

Откройте в браузере:
```
https://smart-signal-backend.onrender.com/docs
```

Вы должны увидеть документацию FastAPI (Swagger UI).

### WebSocket

Проверьте WebSocket подключение:
```javascript
const ws = new WebSocket('wss://smart-signal-backend.onrender.com/ws');
ws.onopen = () => console.log('Connected!');
```

### Mini App

1. Откройте вашего бота в Telegram
2. Нажмите кнопку меню
3. Вы должны увидеть интерфейс с надписью "Ожидание сигналов..."
4. Через 15-30 секунд должны начать приходить сигналы

## Решение проблем

### Backend не запускается

- Проверьте логи в Render Dashboard
- Убедитесь, что все файлы из папки `backend` загружены в репозиторий
- Проверьте, что `Root Directory` = `backend`

### WebSocket не подключается

- Убедитесь, что используете `wss://` (не `ws://`)
- Проверьте CORS настройки в `backend/main.py`
- Проверьте переменную `VITE_WS_URL` в настройках Static Site

### Сигналы не приходят

- Дождитесь 30-60 секунд после запуска
- Проверьте логи backend в Render Dashboard
- Убедитесь, что Binance WebSocket работает (проверьте логи)

### Mini App не открывается в Telegram

- Убедитесь, что URL правильный в BotFather
- Проверьте, что Static Site успешно задеплоился
- Попробуйте открыть URL напрямую в браузере

## Обновление приложения

После изменений в коде:

1. Сделайте `git push` в ваш репозиторий
2. Render автоматически пересоберёт и задеплоит приложения
3. Обновите Mini App в Telegram (закройте и откройте заново)

## Бесплатный план Render.com

На бесплатном плане:

- Backend может "засыпать" после 15 минут неактивности
- Первый запрос после сна займёт 30-60 секунд
- Для продакшена рекомендуется платный план ($7/мес)

## Полезные ссылки

- [Render Dashboard](https://dashboard.render.com)
- [Render Docs](https://render.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
