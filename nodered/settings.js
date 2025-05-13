module.exports = {
    flowFile: 'flows.json',
    flowFilePretty: true,
    uiPort: process.env.PORT || 1880,
    mqttReconnectTime: 15000,
    serialReconnectTime: 15000,
    debugMaxLength: 1000,
    functionGlobalContext: {
        os: require('os')
    },
    exportGlobalContextKeys: false,
    logging: {
        console: {
            level: "info",
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