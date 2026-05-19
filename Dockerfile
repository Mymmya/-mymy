FROM ubuntu:22.04

# Отключаем интерактивные окна при установке
ENV DEBIAN_FRONTEND=noninteractive

# Ставим только Python, pip и базовые системные библиотеки
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем абсолютно все файлы проекта в директорию /app
COPY . .

# Устанавливаем зависимости Python, если есть requirements.txt
RUN if [ -f requirements.txt ]; then pip3 install --no-cache-dir -r requirements.txt; fi

# ВАЖНО: Замените 'main.py' на реальное имя вашего файла, если он называется по-другому!
CMD ["python3", "main.py"]
