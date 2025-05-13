FROM python:3.9-slim

WORKDIR /app

# Instalação das dependências mínimas necessárias
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Instalação dos pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do simulador
COPY . .

# Comando de execução
CMD ["python", "main.py"] 