# Imagen base mínima compatible con Rasa 3.6
FROM python:3.10-alpine

# Carpeta de trabajo
WORKDIR /app
COPY . /app

# Instala dependencias básicas necesarias para compilar (sin cache)
RUN apk add --no-cache build-base g++ git

# Actualiza pip y setuptools, instala dependencias sin guardar caché (reduce >1GB)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Permisos al script de arranque
RUN chmod +x start.sh

# Exponer puerto del servidor Rasa
EXPOSE 5005

# Comando de inicio del bot
CMD ["./start.sh"]
