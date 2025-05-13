-- Criação da tabela para registrar o status do robô
CREATE TABLE IF NOT EXISTS robot_status (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela para registrar comandos enviados ao robô
CREATE TABLE IF NOT EXISTS robot_commands (
    id SERIAL PRIMARY KEY,
    command VARCHAR(20) NOT NULL,
    position_x FLOAT,
    position_y FLOAT,
    position_z FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela para registrar respostas do sistema supervisório
CREATE TABLE IF NOT EXISTS supervisor_responses (
    id SERIAL PRIMARY KEY,
    command_id INTEGER REFERENCES robot_commands(id),
    response VARCHAR(20) NOT NULL,
    reason TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhorar performance de consultas
CREATE INDEX idx_robot_status_timestamp ON robot_status(timestamp);
CREATE INDEX idx_robot_commands_timestamp ON robot_commands(timestamp);
CREATE INDEX idx_supervisor_responses_command_id ON supervisor_responses(command_id);

-- Comentários nas tabelas
COMMENT ON TABLE robot_status IS 'Armazena o histórico de status do robô UR5';
COMMENT ON TABLE robot_commands IS 'Armazena os comandos enviados ao robô UR5';
COMMENT ON TABLE supervisor_responses IS 'Armazena as respostas do sistema supervisório aos comandos do robô'; 