FROM ubuntu:22.04

# Установка SSH-сервера и базовых утилит
RUN apt-get update && apt-get install -y openssh-server curl git wget && \
    mkdir /var/run/sshd

# Устанавливаем пароль 114411 для пользователя root
RUN echo 'root:114411' | chpasswd

# Разрешаем вход по паролю и напрямую для root-пользователя
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
