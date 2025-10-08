#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Mostrar contenido del directorio models
ls models

# Ejecutar servidor Rasa
rasa run -m models/20251002-142542-similar-delta.tar.gz --enable-api --cors "*" --host 0.0.0.0 --port ${PORT:-8080} --credentials credentials.yml --endpoints endpoints.yml
