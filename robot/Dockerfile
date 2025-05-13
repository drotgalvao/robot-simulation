FROM python:3.9-slim

WORKDIR /app

# Instalação das dependências para X11 e visualização
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    xvfb \
    x11-utils \
    libx11-dev \
    novnc \
    websockify \
    x11vnc \
    git \
    wget \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Instalação do noVNC de forma correta
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc && \
    cd /opt/novnc && \
    git checkout v1.3.0 && \
    ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# Instalação dos pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do simulador
COPY . .

# Configura variáveis de ambiente para display X11
ENV DISPLAY=:1

# Inicia Xvfb, x11vnc e a aplicação
ENTRYPOINT ["sh", "-c", "Xvfb :1 -screen 0 1024x768x24 -ac +extension GLX +render -noreset & \
                          x11vnc -display :1 -nopw -listen localhost -xkb -forever & \
                          /opt/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 80 & \
                          python main.py"] 