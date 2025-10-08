# Imagen base ligera con Python 3.9
FROM python:3.9-slim

# Configura directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará Rasa
ENV PORT=5005
EXPOSE 5005

# Comando de arranque directo
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "5005", "-m", "models"]
