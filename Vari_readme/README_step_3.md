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
- **main.yml**: ci sono all interno le task da eseguire per decidere quale motere tra docker e podman utilizzare
- **docker.yml**: si trovano le task principali da eseguire se viene utilizzato docker
- **podman.yml**: si trovano le task principali da eseguire se viene utilizzato podman