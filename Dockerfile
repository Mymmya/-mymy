FROM ubuntu:22.04

# Отключаем интерактивные окна
ENV DEBIAN_FRONTEND=noninteractive

# Ставим только Python, pip и базовые утилиты (чтобы проверить файлы)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем текущие файлы (посмотрим, что именно долетает до сервера)
COPY . .

# Бесконечный сон, чтобы контейнер не умирал и держал SSH-сессию активной
CMD ["sleep", "infinity"]
