# Obbiettivo
## Creare un playbook che configuri un docker registry (anche senza autenticazione)

Questo playbook Ansible configura ed avvia un Docker Registry locale sulla macchina host senza autenticazione. Il registry memorizzerà i dati persistenti in una directory specificata.
## Spiegazione task playbook

### Task:
```yaml
    - name: Creazione della directory per i dati del registro
      file:
        path: "{{ docker_registry_data_path }}"
        state: directory
```
viene creata una directory locale dove memorizzare i file.

### Task:
```yaml
    - name: Avviare il container Docker Registry
      community.docker.docker_container:
        name: registry
        image: registry:2
        state: started
        restart_policy: always
        ports:
          - "{{ docker_registry_port }}:5000"
        volumes:
          - "{{ docker_registry_data_path }}:/var/lib/registry"
```
andiamo a creare il container registry.
