FROM debian:latest

RUN apt-get update && \
    apt-get install -y openssh-server sudo && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    echo 'AllowUsers genericuser' >> /etc/ssh/sshd_config

RUN useradd -m genericuser
RUN mkdir -p /home/genericuser/.ssh && \
    chown genericuser:genericuser /home/genericuser/.ssh

RUN echo "genericuser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/genericuser \
    && chmod 0440 /etc/sudoers.d/genericuser

COPY id_rsa.pub /home/genericuser/.ssh/authorized_keys
RUN chown genericuser:genericuser /home/genericuser/.ssh/authorized_keys && \
    chmod 700 /home/genericuser/.ssh && \
    chmod 600 /home/genericuser/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
