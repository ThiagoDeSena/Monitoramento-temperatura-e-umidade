import time
time.sleep(10) 
from databases import Database
from mqttClient import MqttClient
from dataProcessor import DataProcessor
from graphGenerator import GraphGenerator
import threading



# Loop para o gráfico ser sempre atualizado
def update_graph_periodically():
    while True:
        graphGenerator.update_graph()
        time.sleep(30)  # Espera 30 segundos

#Cria um objeto da classe DAtabase
db = Database(host="localhost",user="user01",password="pi",database="monitoramento")

data_processor = DataProcessor(db)
mqtt_client = MqttClient("10.0.0.105",data_processor=data_processor)

graphGenerator = GraphGenerator(db)
graphGenerator.update_graph()

# Cria uma thead para atualizar o gráfico
update_thread = threading.Thread(target=update_graph_periodically)
update_thread.start()

mqtt_client.start()







