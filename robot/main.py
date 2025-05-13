import os
import time
import json
import pybullet as p
import pybullet_data
import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do MQTT
MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC_STATUS = "robot/status"
MQTT_TOPIC_COMMAND = "robot/command"
MQTT_TOPIC_RESPONSE = "robot/response"

# Limites do espaço de trabalho do robô
WORKSPACE_LIMITS = {
    "x_min": float(os.getenv("ROBOT_WORKSPACE_LIMITS_X_MIN", -0.6)),
    "x_max": float(os.getenv("ROBOT_WORKSPACE_LIMITS_X_MAX", 0.6)),
    "y_min": float(os.getenv("ROBOT_WORKSPACE_LIMITS_Y_MIN", -0.6)),
    "y_max": float(os.getenv("ROBOT_WORKSPACE_LIMITS_Y_MAX", 0.6)),
    "z_min": float(os.getenv("ROBOT_WORKSPACE_LIMITS_Z_MIN", 0.0)),
    "z_max": float(os.getenv("ROBOT_WORKSPACE_LIMITS_Z_MAX", 0.6))
}

class UR5Simulator:
    def __init__(self):
        # Inicializa o PyBullet em modo GUI
        p.connect(p.GUI)  # Modo GUI para visualização 3D
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # Desativa os controles GUI para simplificar a interface
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        
        # Carrega o plano
        self.plane_id = p.loadURDF("plane.urdf")
        
        # Tenta carregar o modelo UR5 do arquivo local
        try:
            self.robot_id = p.loadURDF("ur5.urdf", [0, 0, 0], useFixedBase=True)
            print("Modelo UR5 carregado com sucesso")
        except Exception as e:
            print(f"Erro ao carregar modelo UR5: {e}")
            try:
                # Tenta carregar o KUKA como alternativa
                self.robot_id = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)
                print("Modelo KUKA carregado com sucesso (fallback)")
            except Exception as e2:
                print(f"Erro ao carregar modelo KUKA: {e2}")
                try:
                    # Tenta carregar o Panda como segunda alternativa
                    self.robot_id = p.loadURDF("franka_panda/panda.urdf", [0, 0, 0], useFixedBase=True)
                    print("Modelo Panda carregado com sucesso (fallback)")
                except Exception as e3:
                    print(f"Erro ao carregar modelo Panda: {e3}")
                    raise RuntimeError("Não foi possível carregar nenhum modelo de robô")
        
        # Obtém informações sobre as juntas do robô
        self.num_joints = p.getNumJoints(self.robot_id)
        self.joint_ids = []
        self.joint_names = []
        
        for i in range(self.num_joints):
            joint_info = p.getJointInfo(self.robot_id, i)
            if joint_info[2] == p.JOINT_REVOLUTE:
                self.joint_ids.append(i)
                self.joint_names.append(joint_info[1].decode('utf-8'))
        
        # Posição inicial
        self.current_position = {"x": 0.0, "y": 0.4, "z": 0.4}
        self.move_to_position(self.current_position["x"], self.current_position["y"], self.current_position["z"])
        
        # Inicializa MQTT
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        # Tenta conectar ao MQTT com retry
        max_retries = 10
        retry_count = 0
        connected = False
        
        while not connected and retry_count < max_retries:
            try:
                print(f"Tentando conectar ao MQTT broker {MQTT_HOST}:{MQTT_PORT} (tentativa {retry_count+1})")
                self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
                connected = True
                print("Conectado ao MQTT broker com sucesso")
            except Exception as e:
                print(f"Erro ao conectar ao MQTT: {e}")
                retry_count += 1
                time.sleep(5)  # Espera 5 segundos antes de tentar novamente
        
        if not connected:
            raise RuntimeError("Não foi possível conectar ao broker MQTT após várias tentativas")
        
        self.mqtt_client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado ao broker MQTT com código de resultado {rc}")
        self.mqtt_client.subscribe(MQTT_TOPIC_COMMAND)
        self.mqtt_client.subscribe(MQTT_TOPIC_RESPONSE)
        
        # Envia status inicial
        self.publish_status("iniciado", "Simulador do robô iniciado")
        
    def on_message(self, client, userdata, msg):
        try:
            message = json.loads(msg.payload)
            print(f"Mensagem recebida no tópico {msg.topic}: {message}")
            
            if msg.topic == MQTT_TOPIC_COMMAND:
                if "command" in message and message["command"] == "move":
                    if "x" in message and "y" in message and "z" in message:
                        self.execute_movement(message["x"], message["y"], message["z"])
                    else:
                        self.publish_status("erro", "Comando de movimento incompleto")
                        
            elif msg.topic == MQTT_TOPIC_RESPONSE:
                if "response" in message:
                    if message["response"] == "approved":
                        print("Movimento aprovado pelo supervisor")
                    elif message["response"] == "rejected":
                        print("Movimento rejeitado pelo supervisor")
                        self.publish_status("rejeitado", "Movimento rejeitado pelo supervisor")
                        
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {msg.payload}")
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
    
    def is_position_valid(self, x, y, z):
        if (x < WORKSPACE_LIMITS["x_min"] or x > WORKSPACE_LIMITS["x_max"] or
            y < WORKSPACE_LIMITS["y_min"] or y > WORKSPACE_LIMITS["y_max"] or
            z < WORKSPACE_LIMITS["z_min"] or z > WORKSPACE_LIMITS["z_max"]):
            return False
        return True
    
    def execute_movement(self, x, y, z):
        x, y, z = float(x), float(y), float(z)
        
        if not self.is_position_valid(x, y, z):
            self.publish_status("erro", f"Posição ({x}, {y}, {z}) fora dos limites de trabalho")
            return
        
        self.publish_status("movendo", f"Iniciando movimento para ({x}, {y}, {z})")
        
        try:
            self.move_to_position(x, y, z)
            self.current_position = {"x": x, "y": y, "z": z}
            self.publish_status("sucesso", f"Movimento concluído para ({x}, {y}, {z})")
        except Exception as e:
            self.publish_status("erro", f"Erro durante movimento: {str(e)}")
    
    def move_to_position(self, x, y, z):
        target_position = [x, y, z]
        
        # Usa a cinemática inversa para calcular os ângulos das juntas
        target_orientation = p.getQuaternionFromEuler([0, -np.pi, 0])
        joint_positions = p.calculateInverseKinematics(
            self.robot_id, 
            self.joint_ids[-1], 
            target_position, 
            target_orientation
        )
        
        # Move as juntas para a posição calculada
        for i, joint_id in enumerate(self.joint_ids):
            p.setJointMotorControl2(
                bodyIndex=self.robot_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=joint_positions[i],
                force=500
            )
        
        # Aguarda o movimento ser concluído
        for _ in range(100):  # Simula por alguns passos
            p.stepSimulation()
            time.sleep(0.01)
            
    def publish_status(self, status, message):
        payload = {
            "status": status,
            "position": self.current_position,
            "message": message,
            "timestamp": time.time()
        }
        self.mqtt_client.publish(MQTT_TOPIC_STATUS, json.dumps(payload))
        print(f"Status publicado: {payload}")
        
    def run(self):
        try:
            while True:
                p.stepSimulation()
                time.sleep(0.1)  # Reduzido para economizar CPU no modo headless
        except KeyboardInterrupt:
            print("Simulação interrompida pelo usuário")
        finally:
            self.mqtt_client.loop_stop()
            p.disconnect()
            print("Simulação encerrada")

if __name__ == "__main__":
    try:
        simulator = UR5Simulator()
        simulator.run()
    except Exception as e:
        print(f"Erro fatal na simulação: {e}")
        import traceback
        traceback.print_exc() 