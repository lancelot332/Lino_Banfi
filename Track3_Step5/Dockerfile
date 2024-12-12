# Usa l'immagine Alpine come base
FROM alpine:latest

# Aggiungi un maintainer (opzionale)
LABEL maintainer="tuo_nome@esempio.com"

# Aggiorna i pacchetti e installa dipendenze necessarie (ad esempio, curl e bash)
RUN apk update && apk add --no-cache bash curl

# Crea una directory di lavoro
WORKDIR /app

# Copia il file di configurazione o il codice nell'immagine (opzionale)
#COPY ./src /app

# Imposta la variabile d'ambiente (opzionale)
ENV APP_ENV=production

# Esegui un comando di esempio (esempio: bash)
CMD ["bash"]
