/**
 * Script para escutar mensagens MQTT e inserir no PostgreSQL
 * Este script deve ser executado diretamente e ficará em execução
 */

const { Pool } = require('pg');
const mqtt = require('mqtt');

// Configuração da conexão PostgreSQL
const pgConfig = {
  user: process.env.POSTGRES_USER || 'robotuser',
  host: process.env.POSTGRES_HOST || 'postgres',
  database: process.env.POSTGRES_DB || 'robotdb',
  password: process.env.POSTGRES_PASSWORD || 'robotpass',
  port: 5432,
};

console.log("Configuração PostgreSQL:", pgConfig);

// Configuração MQTT
const mqttConfig = {
  host: process.env.MQTT_HOST || 'mqtt',
  port: process.env.MQTT_PORT || 1883,
  clientId: 'mqtt-postgres-bridge-' + Math.random().toString(16).substring(2, 8)
};

console.log("Configuração MQTT:", mqttConfig);

// Inicializar pool de conexão PostgreSQL
const pool = new Pool(pgConfig);

// Monitorar erros na conexão PostgreSQL
pool.on('error', (err) => {
  console.error('Erro no pool PostgreSQL:', err);
});

// Conexão ao broker MQTT
const mqttClient = mqtt.connect(`mqtt://${mqttConfig.host}:${mqttConfig.port}`, {
  clientId: mqttConfig.clientId
});

// Ao conectar ao MQTT
mqttClient.on('connect', () => {
  console.log('Conectado ao broker MQTT');
  
  // Assinar tópicos relevantes
  mqttClient.subscribe('robot/status', (err) => {
    if (!err) {
      console.log('Inscrito no tópico robot/status');
    } else {
      console.error('Erro ao inscrever-se no tópico robot/status:', err);
    }
  });
  
  mqttClient.subscribe('robot/command', (err) => {
    if (!err) {
      console.log('Inscrito no tópico robot/command');
    } else {
      console.error('Erro ao inscrever-se no tópico robot/command:', err);
    }
  });
});

// Lidar com mensagens recebidas
mqttClient.on('message', async (topic, message) => {
  console.log(`Mensagem recebida no tópico ${topic}`);
  
  try {
    // Converter mensagem para objeto JSON
    const data = JSON.parse(message.toString());
    
    // Inserir dados no PostgreSQL dependendo do tópico
    if (topic === 'robot/status') {
      await insertRobotStatus(data);
    } else if (topic === 'robot/command') {
      await insertRobotCommand(data);
    }
  } catch (err) {
    console.error(`Erro ao processar mensagem do tópico ${topic}:`, err);
  }
});

// Função para inserir status do robô no PostgreSQL
async function insertRobotStatus(data) {
  try {
    const client = await pool.connect();
    
    try {
      const sql = "INSERT INTO robot_status (status, position_x, position_y, position_z, message) VALUES ($1, $2, $3, $4, $5) RETURNING id";
      const params = [data.status, data.position.x, data.position.y, data.position.z, data.message];
      
      const result = await client.query(sql, params);
      console.log(`Status do robô inserido no PostgreSQL. ID: ${result.rows[0].id}`);
    } finally {
      client.release();
    }
  } catch (err) {
    console.error('Erro ao inserir status do robô no PostgreSQL:', err);
  }
}

// Função para inserir comando do robô no PostgreSQL
async function insertRobotCommand(data) {
  try {
    const client = await pool.connect();
    
    try {
      const sql = "INSERT INTO robot_commands (command, position_x, position_y, position_z) VALUES ($1, $2, $3, $4) RETURNING id";
      const params = [data.command, data.x, data.y, data.z];
      
      const result = await client.query(sql, params);
      console.log(`Comando do robô inserido no PostgreSQL. ID: ${result.rows[0].id}`);
    } finally {
      client.release();
    }
  } catch (err) {
    console.error('Erro ao inserir comando do robô no PostgreSQL:', err);
  }
}

// Tratar interrupções
process.on('SIGINT', async () => {
  console.log('Encerrando script...');
  
  // Fechar conexão MQTT
  mqttClient.end();
  console.log('Conexão MQTT encerrada');
  
  // Fechar pool de conexão PostgreSQL
  await pool.end();
  console.log('Pool PostgreSQL encerrado');
  
  process.exit(0);
}); 