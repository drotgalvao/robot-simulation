FROM nodered/node-red:latest

# Diretório de trabalho
WORKDIR /data

# Atualiza o NPM e instala o pg para garantir suporte ao PostgreSQL
RUN npm install -g npm@latest && \
    npm install --unsafe-perm pg

# Instala os nós necessários para o Node-RED
RUN npm install --unsafe-perm --no-update-notifier --no-fund --only=production \
    node-red-dashboard \
    node-red-node-ui-table \
    node-red-contrib-ui-svg \
    node-red-contrib-postgresql@0.13.0 \
    node-red-contrib-mqtt-broker

# Expõe as portas necessárias
EXPOSE 1880 1881

# Copia os arquivos
COPY flows.json /data/flows.json
COPY settings.js /data/settings.js
COPY package.json /data/package.json
COPY test-db-connection.js /data/test-db-connection.js

# Script de inicialização
ENTRYPOINT ["npm", "start", "--", "--userDir", "/data"] 