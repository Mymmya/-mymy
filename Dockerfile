FROM python:3.10-slim

# Устанавливаем зависимости для SSH, сети и скачивания файлов
RUN apt-get update && apt-get install -y \
    openssh-server \
    curl \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем SSH: разрешаем вход root с твоим паролем
RUN mkdir /var/run/sshd \
    && echo 'root:vlLHA2AYeFnFKOjf' | chpasswd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Создаем рабочую директорию
WORKDIR /app

# Скачиваем твой тестовый скрипт из GitHub и переименовываем в main.py
RUN curl -L https://raw.githubusercontent.com/Mymmya/-mymy/main/testt_bot.py -o main.py

# Устанавливаем aiogram
RUN pip install --no-cache-dir aiogram

# Открываем 22 порт для SSH
EXPOSE 22

# Запускаем SSH-сервис и следом бота
CMD service ssh start && python main.py
