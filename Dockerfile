# Imagen base ligera con Python 3.9
FROM python:3.9-slim

# Evitar prompts y forzar salida directa
ENV PYTHONUNBUFFERED=1

# Configura el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . /app

# Instala dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará Rasa
EXPOSE 5005
ENV PORT=5005

# Comando de arranque
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "5005", "--credentials", "credentials.yml", "--endpoints", "endpoints.yml"]

