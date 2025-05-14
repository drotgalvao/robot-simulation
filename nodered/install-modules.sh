#!/bin/bash

cd /data
npm install --unsafe-perm --no-update-notifier --no-fund \
    node-red-dashboard \
    node-red-node-ui-table \
    node-red-contrib-ui-svg \
    node-red-contrib-postgresql@0.13.0 \
    node-red-contrib-mqtt-broker

# Verificação de instalação
if [ $? -ne 0 ]; then
    echo "Erro na instalação dos módulos Node-RED"
    exit 1
fi

echo "Módulos instalados com sucesso!" 