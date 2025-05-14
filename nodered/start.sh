#!/bin/bash

# Instalação dos módulos
echo "Instalando módulos..."
chmod +x /data/install-modules.sh
/data/install-modules.sh

# Iniciar o bridge MQTT para PostgreSQL em background
echo "Iniciando bridge MQTT para PostgreSQL..."
node /data/mqtt-to-db.js > /data/mqtt-to-db.log 2>&1 &
BRIDGE_PID=$!
echo "Bridge iniciado com PID: $BRIDGE_PID"

# Garantir que o PID foi salvo
echo $BRIDGE_PID > /data/bridge.pid

# Iniciar o Node-RED em foreground
echo "Iniciando Node-RED..."
exec npm start -- --userDir /data 