# Imagen base más ligera, ya contiene Rasa preinstalado
FROM rasa/rasa:3.6.20-spacy

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Desactiva la telemetría de Rasa (reduce logs y procesos extra)
ENV RASA_TELEMETRY_ENABLED=false

# Instala dependencias adicionales de tu bot
RUN pip install --upgrade pip==24.2 setuptools wheel && \
    pip install -r requirements.txt

# Da permisos de ejecución al script de inicio
RUN chmod +x start.sh

# Expone el puerto que usa Rasa
EXPOSE 5005

# Comando para iniciar el bot
CMD ["./start.sh"]
