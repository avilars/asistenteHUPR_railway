# Imagen base oficial de Rasa 3.6.20
FROM rasa/rasa:3.6.20

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Desactiva telemetría (opcional)
ENV RASA_TELEMETRY_ENABLED=false

# Elimina TensorFlow para reducir tamaño
RUN pip uninstall -y tensorflow tensorflow-intel tensorflow-estimator || true

# Instala tus dependencias
RUN pip install --upgrade pip==24.2 setuptools wheel && \
    pip install -r requirements.txt || true && \
    pip cache purge || true

# Da permisos al script de inicio
RUN chmod +x start.sh

# Expone el puerto
EXPOSE 5005

# Comando por defecto
CMD ["./start.sh"]
