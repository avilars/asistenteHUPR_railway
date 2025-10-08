import os
from rasa.__main__ import main as rasa_main

if __name__ == "__main__":
    port = os.getenv("PORT", "5005")
    print(f"[start_render.py] Arrancando Rasa en puerto {port}...")
    args = [
        "run",
        "--enable-api",
        "--cors", "*",
        "--host", "0.0.0.0",
        "--port", port,
        "-m", "models",
        "--credentials", "credentials.yml",
        "--endpoints", "endpoints.yml"
    ]
    rasa_main(args)
