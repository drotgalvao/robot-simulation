/**
 * Copyright JS Foundation and other contributors, http://js.foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 **/

module.exports = {
    flowFile: 'flows.json',
    flowFilePretty: true,
    uiPort: process.env.PORT || 1880,
    mqttReconnectTime: 15000,
    serialReconnectTime: 15000,
    debugMaxLength: 1000,
    
    // IMPORTANTE: Carga do módulo personalizado PostgreSQL
    httpNodeMiddleware: function(req, res, next) {
        next();
    },
    
    // Script de inicialização para o DB PostgreSQL
    httpAdminMiddleware: function(req, res, next) {
        next();
    },
    
    // Script para ser carregado na inicialização
    externalModules: {
        autoInstall: true,
        palette: {
            allowInstall: true,
            allowUpload: true
        }
    },
    
    // Objetos que estarão disponíveis no contexto global
    functionGlobalContext: {
        os: require('os'),
        process: process,
        env: process.env
    },
    functionExternalModules: true,
    
    // Sem script de inicialização automática
    
    exportGlobalContextKeys: false,
    logging: {
        console: {
            level: "debug",
            metrics: false,
            audit: false
        }
    },
    editorTheme: {
        projects: {
            enabled: false
        }
    },
    dashboardUI: {
        port: 1881
    },
    contextStorage: {
        default: "memoryOnly",
        memoryOnly: { module: 'memory' }
    },
    credentialSecret: "roboticarur5segurasimulacao2025"
};