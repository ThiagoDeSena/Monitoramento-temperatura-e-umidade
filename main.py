import time
time.sleep(10) 
from databases import Database
from mqttClient import MqttClient
from dataProcessor import DataProcessor
from graphGenerator import GraphGenerator

#Variável de controle para o loop MQTT
mqtt_started=False

#Cria um objeto da classe DAtabase
db = Database(host="localhost",user="user01",password="pi",database="monitoramento")


data_processor = DataProcessor(db)
mqtt_client = MqttClient("broker.hivemq.com",data_processor=data_processor)
graphGenerator = GraphGenerator(db,mqtt_client)

graphGenerator.update_graph()
graphGenerator.publish_button()

#Garante que o loop do MQTT vai ser inicializado apenas uma vez
if not mqtt_started:
    print("Loop MQTT iniciado!")
    mqtt_client.start()
    mqtt_started=True

