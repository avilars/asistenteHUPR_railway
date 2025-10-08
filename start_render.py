import os
import subprocess

port = os.getenv("PORT", "5005")
print(f"[start_render.py] Arrancando Rasa en puerto {port}...")

cmd = [
    "rasa",
    "run",
    "--enable-api",
    "--cors",
    "*",
    "--host",
    "0.0.0.0",
    "--port",
    port,
    "-m",
    "models",
    "--credentials",
    "credentials.yml",
    "--endpoints",
    "endpoints.yml",
]

subprocess.run(cmd)
