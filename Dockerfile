FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y build-essential gcc g++ git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip==24.2 setuptools wheel && \
    pip install -r requirements.txt

# EXPOSE y CMD al final
EXPOSE 5005
CMD ["./start.sh"]
