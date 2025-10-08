import os
import subprocess

print("[start_render.py] Arrancando Rasa en puerto 5005...")

subprocess.run([
    "rasa", "run",
    "--enable-api",
    "--cors", "*",
    "--host", "0.0.0.0",
    "--port", "5005",
    "-m", f"models/{sorted(os.listdir('models'))[-1]}",
    "--credentials", "credentials.yml",
    "--endpoints", "endpoints.yml"
])
