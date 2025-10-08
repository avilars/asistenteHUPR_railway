FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Instala dependencias del sistema necesarias para compilar Rasa
RUN apt-get update && apt-get install -y build-essential gcc g++ git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala pip y dependencias del bot
RUN pip install --upgrade pip==24.2 setuptools wheel && \
    pip install -r requirements.txt

# Da permisos al script de inicio
RUN chmod +x start.sh

# Expone el puerto que usa Railway automáticamente
EXPOSE 5005

# Ejecuta el script de inicio del bot
CMD ["./start.sh"]
