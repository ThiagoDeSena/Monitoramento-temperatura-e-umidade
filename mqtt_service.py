from databases import Database
from mqttClient import MqttClient
from dataProcessor import DataProcessor
import time

# Aguarda o MariaDB iniciar (caso rode via boot)
time.sleep(10)

# Cria o banco, processador de dados e MQTT
db = Database(host="localhost", user="user01", password="pi", database="monitoramento")
data_processor = DataProcessor(db)
mqtt_client = MqttClient("localhost", data_processor=data_processor)

# Inicia o loop do MQTT (vai rodar para sempre)
print("Iniciando loop MQTT no serviço separado...")
mqtt_client.start()

# Mantém o script vivo (loop_start já roda em background)
while True:
    time.sleep(60)