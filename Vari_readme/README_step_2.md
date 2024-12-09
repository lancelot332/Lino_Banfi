# Obbiettivi

1. Utilizzando Ansible, creare dei playbooks che fanno la build di almeno due container con OS differenti
2. Queste build devono generare dei container che abbiano queste caratteristiche:
- Esser sempre in ascolto sulla porta 22 del container
- Avere attivo il servizio ssh
- Avere un utente abilitato a collegarsi tramite ssh key e poter fare sudo

## Spiegazione task playbook:
questo playbook crea 2 container con 2 sistemi operativi differenti utilizzando 2 dockerfile che sono stati configurati in modo che si possano connetere tramite ssh con la macchina host.

### Tasks:
```yaml
    - name: Create directories for Dockerfiles
      file:
        path: "{{ item }}"
        state: directory
      with_items:
        - ./debian_container
        - ./ubuntu_container

    - name: Copy Dockerfile for Debian
      copy:
        src: files/Dockerfile_debian
        dest: ./debian_container/Dockerfile

    - name: Copy id_rsa for Debian
      copy:
        src: files/id_rsa.pub
        dest: ./debian_container

    - name: Copy Dockerfile for Ubuntu
      copy:
        src: files/Dockerfile_ubuntu
        dest: ./ubuntu_container/Dockerfile

    - name: Copy id_rsa for Ubuntu
      copy:
        src: files/id_rsa.pub
        dest: ./ubuntu_container
```
con le seguenti task andiamo a creare le directory che conterrano i file necessari per la creazione dei 2 container, in seguito andiamo a copiare i rispettivi dockerfile e la chiave pubblica all' interno delle directory

### Tasks:
```yaml
    - name: Build Debian container
      docker_image:
        source: build
        build:
          path: ./debian_container
        name: debian_ssh

    - name: Build Ubuntu container
      docker_image:
        source: build
        build:
          path: ./ubuntu_container
        name: ubuntu_ssh

    - name: Run Debian container
      docker_container:
        name: debian_ssh
        image: debian_ssh
        state: started
        ports:
          - "2222:22"

    - name: Run Ubuntu container
      community.docker.docker_container:
        name: ubuntu_ssh
        image: ubuntu_ssh
        state: started
        ports:
          - "2223:22"
```
con  queste task invece andiamo a buildare le immagini e a creare i container con le immagini appena buildate.

## Spiegazione dockerfile:

### Dockerfile debian:
```dockerfile
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
```

### Dockerfile ubuntu:
```dockerfile
FROM ubuntu:latest

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
```