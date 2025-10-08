# Imagen base
FROM python:3.9-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Da permisos al script de inicio
RUN chmod +x start.sh

# Expone el puerto 5005 (para Railway)
ENV PORT=5005
EXPOSE 5005

# Comando de arranque
CMD ["bash", "start.sh"]
