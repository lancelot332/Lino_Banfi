# Obbiettivo

## Utilizzare Ansible Vault per oscurare tutte le password (come quella degli utenti nei Dockerfile o user e password per il registry)

## Spiegazione 

1. Ho creato un vault con le password per gli account degli utenti e per il login del registry utilizzando il seguente comando:      
`ansible-vault create vault`
2. Ho modificato il playbook caricando la variabile vault
```yaml
---
- hosts: localhost
  vars_files:
    - vault.yml
    
  roles:
    - registry
    - build_containers
    - push_to_registry
    - run_containers
```
3. Ho inserito nel role per il registry l autenticazione cosi che possiamo utilizzare il vault  
Tasks:
```yaml
---

- name: Generare il file htpasswd per il registry
  ansible.builtin.command:
    cmd: >
      htpasswd -Bbn "{{ registry_user }}" "{{ registry_password }}"
  register: htpasswd_output

- name: Scrivere il file htpasswd
  ansible.builtin.copy:
    dest: /Users/lorenzomoro/registry/auth/htpasswd
    content: "{{ htpasswd_output.stdout }}"

- name: Start container registry con autenticazione
  community.docker.docker_container:
    name: registry
    image: registry:2
    state: started
    restart_policy: always
    ports:
      - "5000:5000"
    volumes:
      - "/Users/lorenzomoro/registry:/var/lib/registry"
      - "/Users/lorenzomoro/registry/auth:/auth"
    env:
      REGISTRY_AUTH: "htpasswd"
      REGISTRY_AUTH_HTPASSWD_REALM: "Registry Realm"
      REGISTRY_AUTH_HTPASSWD_PATH: "/auth/htpasswd"
```
4. ho modificato i dockerfile aggiungendo la variabile per le proprie password  
Dockerfile:
```dockerfile
FROM ubuntu:latest

ARG user1_password

RUN apt update && \
    apt install -y openssh-server sudo

RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    echo 'AllowUsers genericuser' >> /etc/ssh/sshd_config

RUN useradd -m genericuser \
    && echo "genericuser:${user1_password}" | chpasswd

RUN echo "genericuser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/genericuser

RUN mkdir -p /home/genericuser/.ssh && \
    chown genericuser:genericuser /home/genericuser/.ssh
    
COPY id_rsa.pub /home/genericuser/.ssh/authorized_keys

RUN chown genericuser:genericuser /home/genericuser/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
```