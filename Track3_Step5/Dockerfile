# Usa l'immagine di base di Python
FROM python:3.10-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia i file necessari per l'app nel container
COPY requirements.txt ./
COPY app.py ./

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta su cui l'app ascolta
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["python", "app.py"]
