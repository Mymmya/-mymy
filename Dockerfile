FROM ubuntu:22.04 as base

### Stage 1 - add/remove packages ###

RUN mkdir -p /scripts /usr/local/bin

COPY ./container/root/scripts/ /scripts/
COPY ./container/root/usr/local/bin/ /usr/local/bin/

# Добавили установку openssh-server и настройку пароля root:root
RUN /bin/bash -e /scripts/ubuntu_apt_config.sh && \
    /bin/bash -e /scripts/ubuntu_apt_cleanmode.sh && \
    ln -s /scripts/clean_ubuntu.sh /clean.sh && \
    ln -s /scripts/security_updates_ubuntu.sh /security_updates.sh && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    /bin/bash -e /security_updates.sh && \
    apt-get install -yqq \
      curl \
      gpg \
      apt-transport-https \
      openssh-server \
    && \
    /bin/bash -e /scripts/install_s6.sh && \
    /bin/bash -e /scripts/install_goss.sh && \
    # НАСТРОЙКА SSH ПО ПАРОЛЮ
    mkdir -p /var/run/sshd && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    echo "root:root" | chpasswd && \
    # Конец настройки SSH
    apt-get remove --purge -yq \
        curl \
        gpg \
    && \
    /bin/bash -e /clean.sh

COPY ./container/root /

### Stage 2 --- collapse layers ###

FROM scratch
COPY --from=base / .

ENV SIGNAL_BUILD_STOP=99 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_KILL_FINISH_MAXTIME=5000 \
    S6_KILL_GRACETIME=3000

RUN goss -g goss.base.yaml validate

# Открываем стандартный порт SSH
EXPOSE 22

CMD ["/bin/bash", "/run.sh"]
