# Obbiettivo


## Utilizzando i precedenti come task, crea più ruoli Ansibile con le seguenti caratteristiche:

1. Creazione e configurazione di un registry 
2. Build di almeno due container:            
    - Push delle build sul regristy precedentemente creato
    - Run dei container in modo che non vadano in conflitto di porte tra loro.


## Spiegazione 

questo è lo schema dei file e delle cartelle che ho creato per la creazioni dei ruoli:
```bash
Track3_Step3
├── debian_ssh
│   ├── Dockerfile
│   └── id_rsa.pub
├── playbook.yml
├── roles
│   ├── build_containers
│   │   └── tasks
│   │       ├── docker.yml
│   │       ├── main.yml
│   │       └── podman.yml
│   ├── push_to_registry
│   │   └── tasks
│   │       ├── docker.yml
│   │       ├── main.yml
│   │       └── podman.yml
│   ├── registry
│   │   └── tasks
│   │       ├── docker.yml
│   │       ├── main.yml
│   │       └── podman.yml
│   └── run_containers
│       └── tasks
│           ├── docker.yml
│           ├── main.yml
│           └── podman.yml
└── ubuntu_ssh
    ├── Dockerfile
    └── id_rsa.pub
```
all' interno di debian_ssh e ubuntu_ssh si trovano i rispettivi dockerfile e la chiave pubblica per il collegamento ssh.  

All' interno di roles si trovano i file utili per quel determinato ruolo.
- **main.yml**: ci sono all interno le task da eseguire per decidere quale motore tra docker e podman utilizzare
- **docker.yml**: si trovano le task principali da eseguire se viene utilizzato docker
- **podman.yml**: si trovano le task principali da eseguire se viene utilizzato podman

### Task Ruolo Registry:
```yaml
---
- name: Start container registry
  community.docker.docker_container:
    name: registry
    image: registry:2
    state: started
    restart_policy: always
    ports:
      - "5000:5000"
    volumes:
      - "/Users/lorenzomoro/registry:/var/lib/registry"
```
in questa task viene creato un registry senza autenticazione.
### Task Ruolo Build containers:
```yaml
- name: Create image for container 1
  docker_image:
    source: build
    build:
      path: "/Users/lorenzomoro/progetto/ubuntu_ssh"
    name: "localhost:5000/ubuntu_ssh"
    tag: latest

- name: Create image for container 2
  docker_image:
    source: build
    build:
      path: "/Users/lorenzomoro/progetto/debian_ssh"
    name: "localhost:5000/debian_ssh"
    tag: latest
```
Con queste task vengono buildate le immaggini.
### Task Ruolo Push
```yaml
- name: Push image ubuntu_ssh
  community.docker.docker_image:
    name: "localhost:5000/ubuntu_ssh"
    tag: latest
    push: yes
    source: "local"

- name: Push image debian_ssh
  community.docker.docker_image:
    name: "localhost:5000/debian_ssh"
    tag: latest
    push: yes
    source: "local"
```
Con queste tasks vengono pushate sul registry le immagini precedentemente create
### Task Run containers:
```yaml
- name: Start container ubuntu_ssh
  ansible.builtin.docker_container:
    name: ubuntu_ssh
    image: "localhost:5000/ubuntu_ssh:latest"
    ports:
      - "2222:22"
    state: started

- name: Start container debian_ssh
  ansible.builtin.docker_container:
    name: debian_ssh
    image: "localhost:5000/debian_ssh:latest"
    ports:
      - "2223:22"
    state: started
```
Con queste task vengono creati i container con le immagini precedentemente buildate
