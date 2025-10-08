import os
import subprocess

print("[start_render.py] Arrancando Rasa en puerto 5005...")

# Asegurar puerto
port = os.getenv("PORT", "5005")

# Comando completo de ejecución
command = [
    "rasa", "run",
    "--enable-api",
    "--cors", "*",
    "--host", "0.0.0.0",
    "--port", port,
    "--credentials", "credentials.yml",
    "--endpoints", "endpoints.yml"
]

# Ejecutar y mostrar salida en tiempo real
subprocess.run(command)
