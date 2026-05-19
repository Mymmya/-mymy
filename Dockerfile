FROM python:3.10-slim

# Устанавливаем системные зависимости, если они понадобятся
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию (на всякий случай)
WORKDIR /app

# Выполняем твою команду при старте контейнера
CMD ["python3", "-c", "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/Mymmya/-mymy/main/Telegram_bot.py').read())"]
