FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Instala dependencias del sistema necesarias para compilar Rasa
RUN apt-get update && apt-get install -y build-essential gcc g++ git

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools wheel

# Instala las dependencias del bot
RUN pip install -r requirements.txt

# Da permisos al script de inicio
RUN chmod +x start.sh

# Expone el puerto que usa Railway automáticamente
EXPOSE 5005

CMD ["./start.sh"]
