# Simulação de Robôs com Comunicação Supervisória

O objetivo deste trabalho é desenvolver e simular um sistema robótico que integre conceitos de cinemática, controle e supervisão em tempo real.

A proposta inclui a implementação de um robô simulado (articulado ou não) capaz de responder a comandos de posicionamento e reportar suas ações a um sistema supervisório, que será responsável por registrar, validar e exibir essas informações.

## Especificações técnicas

### 1. Simulação robótica

O projeto deve ser desenvolvido em um ambiente de simulação como o PyBullet, utilizando robôs nativos da biblioteca (como o braços robóticos, tipo o UR5) ou modelos alternativos, como robôs móveis (ex: R2D2) ou drones.

- Caso seja utilizado um robô articulado, o sistema deve interpretar comandos de destino no espaço (coordenadas x, y, z) e utilizar métodos de cinemática (direta e/ou inversa) para executar os movimentos ponto a ponto.
- Caso seja utilizado um robô não articulado (como um drone ou robô móvel), é obrigatório incluir obstáculos ou alvos de interação no ambiente. Por exemplo:
  - Um robô móvel deve se deslocar por uma trajetória passando por obstáculos definidos, sem colisões.
  - Um drone deve realizar um trajeto de inspeção, visitando um conjunto de pontos definidos como “bases” e registrar um check-in em cada uma no menor tempo possível.

### 2. Lógica de controle e interação

O robô deve ser capaz de executar seus movimentos em tempo real, conforme coordenadas ou comandos recebidos, com tratamento de erros ou exceções (ex: ponto fora do alcance ou colisão prevista). Ao final de cada ação, o robô deve reportar seu status para o sistema supervisório.

### 3. Sistema supervisório

O sistema supervisório deve ser implementado utilizando o Node-RED (ou ferramenta equivalente), recebendo as informações de estado ou posição do robô via protocolo HTTP, MQTT ou WebSocket. O sistema deverá:

- Validar as informações (ex: posição dentro da área permitida, sucesso na execução da tarefa).
- Registrar os dados (preferencialmente com persistência).
- Exibir as informações em tempo real por meio de um painel (dashboard).

### 4. Interação bidirecional

O supervisório deve responder ao robô com uma confirmação ou rejeição da ação executada. O robô, por sua vez, deve ser capaz de reagir a essa resposta, adaptando seu comportamento.

## Entregas obrigatórias

- **Relatório técnico**:  
Descrever o projeto proposto, objetivos, abordagem adotada, arquitetura do sistema, tecnologias utilizadas, principais decisões de implementação e resultados obtidos.

- **Códigos-fonte comentados**:  
Incluindo os scripts da simulação e o fluxo do sistema supervisório (formato JSON ou equivalente).

- **Vídeo demonstrativo (1~5 minutos)**:  
Mostrando a simulação em execução e a comunicação entre o robô e o sistema supervisório.

## Observações adicionais

- O uso de cinemática inversa ou outro método de controle de movimento deve ser claramente descrito e implementado.
- vocês têm liberdade para expandir a proposta com lógica adicional, inteligência artificial, controle de trajetória, entre outros, desde que cumpram os requisitos mínimos.
