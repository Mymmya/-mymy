FROM ubuntu:22.04

# Отключаем интерактивные окна при установке
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем только Python, pip, SSH и базовые утилиты
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    openssh-server \
    wget \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем SSH-сервер
RUN mkdir /var/run/sshd

# Устанавливаем ваш пароль для пользователя root
RUN echo 'root:vlLHA2AYeFnFKOjf' | chpasswd

# Разрешаем вход по паролю для root и отключаем PAM (чтобы пускало в контейнер)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Открываем 22 порт для SSH подключения
EXPOSE 22

WORKDIR /app

# Копируем проект и устанавливаем зависимости Python, если есть requirements.txt
COPY . .
RUN if [ -f requirements.txt ]; then pip3 install --no-cache-dir -r requirements.txt; fi

# Запускаем SSH-службу и затем ваше Python-приложение
CMD service ssh start && python3 main.py