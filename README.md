# Simulação de Robôs com Comunicação Supervisória (UR5)

Este projeto implementa um sistema de simulação robótica com supervisão em tempo real, utilizando contêineres Docker, para simular o robô UR5 com comunicação bidirecional entre o robô e o sistema supervisório.

## Estrutura do Projeto

O projeto está estruturado nos seguintes componentes:

- **robot**: Simulador do robô UR5 utilizando PyBullet, com interpretação de comandos e cinemática inversa.
- **nodered**: Sistema supervisório visual com dashboard para monitoramento e controle.
- **mqtt**: Broker de mensagens para comunicação em tempo real entre componentes.
- **postgres**: Banco de dados para armazenamento de histórico de operações.

## Requisitos

- Docker e Docker Compose
- Acesso à porta 6080 (VNC)
- Acesso à porta 1880 (Node-RED)
- Acesso à porta 1881 (Dashboard)
- Acesso à porta 1883 (MQTT)
- Acesso à porta 5432 (PostgreSQL)

## Instalação e Execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/drotgalvao/robot-simulation.git
   cd robot-simulation
   ```

2. Inicie os contêineres Docker:
   ```bash
   docker-compose up -d
   ```

3. Acesse as interfaces:
   - **Simulação do robô**: Visualização pelo VNC (porta 6080)
   - **Interface de supervisão**: http://localhost:1880
   - **Dashboard de controle**: http://localhost:1880/ui

## Comunicação entre Componentes

- O robô envia seu status pelo tópico MQTT `robot/status`
- O sistema supervisório envia comandos pelo tópico MQTT `robot/command`
- O sistema supervisório responde com aprovação/rejeição no tópico `robot/response`
- Todos os dados são armazenados no PostgreSQL para histórico e análise

## Interação com o Sistema

1. **Controle do Robô**:
   - Utilize o dashboard para enviar comandos de posição (X, Y, Z)
   - O supervisório valida se a posição está dentro dos limites permitidos
   - O robô executa o movimento utilizando cinemática inversa

2. **Monitoramento**:
   - Visualize o status do robô em tempo real
   - Acompanhe o histórico de comandos e movimentos
   - Observe erros e exceções durante a operação

## Limitações do Espaço de Trabalho

```
X: -1.0 a 1.0 metros
Y: -1.0 a 1.0 metros
Z: 0.0 a 1.0 metros
```

## Licença

Este projeto está licenciado sob a licença MIT. 