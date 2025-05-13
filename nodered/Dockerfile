FROM nodered/node-red:latest

# Diretório de trabalho
WORKDIR /data

# Instala os nós necessários para o Node-RED
RUN npm install --unsafe-perm --no-update-notifier --no-fund --only=production \
    node-red-dashboard \
    node-red-node-ui-table \
    node-red-contrib-ui-svg \
    node-red-contrib-postgresql \
    node-red-contrib-mqtt-broker

# Expõe as portas necessárias
EXPOSE 1880 1881

# Copia os arquivos
COPY flows.json /data/flows.json
COPY settings.js /data/settings.js
COPY package.json /data/package.json 