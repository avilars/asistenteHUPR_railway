FROM python:3.10-slim

# 1️⃣ Establecer directorio de trabajo
WORKDIR /app

# 2️⃣ Copiar archivos del proyecto
COPY . /app

# 3️⃣ Instalar dependencias del sistema necesarias para compilar algunas librerías de Rasa
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4️⃣ Instalar dependencias de Python sin guardar caché (reduce ~1GB)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Dar permisos de ejecución al script de inicio
RUN chmod +x start.sh

# 6️⃣ Exponer puerto de Rasa
EXPOSE 5005

# 7️⃣ Comando de inicio
CMD ["./start.sh"]
