#!/bin/bash
echo "🚀 Iniciando Asistente HUPR en Railway..."

# Crear carpeta de modelos si no existe
mkdir -p models

# Descargar el modelo más reciente si no está presente
if [ ! -f models/20251008-214320-burgundy-band.tar.gz ]; then
  echo "⬇️ Descargando modelo desde GitHub..."
  curl -L -o models/20251008-214320-burgundy-band.tar.gz \
  https://raw.githubusercontent.com/avilars/asistenteHUPR_railway/main/models/20251008-214320-burgundy-band.tar.gz
fi

# Verificar que el modelo existe
if [ -f models/20251008-214320-burgundy-band.tar.gz ]; then
  echo "✅ Modelo encontrado: models/20251008-214320-burgundy-band.tar.gz"
else
  echo "❌ ERROR: No se encontró el modelo. Revisa la URL o sube el modelo manualmente."
  exit 1
fi

# Ejecutar Rasa (manteniendo el orden que funcionaba)
echo "⚙️ Ejecutando servidor Rasa..."
rasa run \
  -m models/20251008-214320-burgundy-band.tar.gz \
  --enable-api \
  --cors "*" \
  --credentials credentials.yml \
  --endpoints endpoints.yml \
  --host 0.0.0.0 \
  --port ${PORT:-5005}
