# Obbiettivo

## Creare un container che oltre ai requisiti dello Step 2 abbia anche le seguenti caratteristiche:
- Avere attivo il servizio Docker/Podman;
## Configurare una pipeline Jenkins che:
- Esegua una build di un'immagine e la tagghi in modo progressivo
- Faccia il push dell'immagine sul registry

1. Per avere il servizio docker attivo in un container ho modificato il dockerflle aggiungendo l' installazione di docker, aggiunto l utente nel gruppo docker e avviato il servizio. Inseguito ho modificato il ruolo relativo allla creazione del container dove ho inserito di eseguirlo in modalità privileggiato cosi da poter utilizzare docker facendo così un Docker in Docker.  
NB:  
Docker in Docker non si fa perchè  
.  
.  
.  
2. ### Spiegazione pipeline:
```groovy
pipeline {
    agent any
    environment {
        REGISTRY_URL = 'localhost:5000'
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                dir('Track3_Step5') {
                    script {
                        def tag = "build-${env.BUILD_NUMBER}"
                        def imageName = "app-prova:${tag}"
                        def image = docker.build(imageName)

                        docker.withRegistry("http://${env.REGISTRY_URL}") {
                            image.push()
                        }

                        sh "docker rmi --force ${imageName}"
                    }
                }
            }
        }
    }
}
```
Con la seguente pipeline vado a definire il tag in modo che sia progressivo, faccio la build dell immagine inserendo il nome e il tag ed in seguito la pusho sul registry.