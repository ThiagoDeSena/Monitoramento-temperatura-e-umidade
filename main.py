import time
time.sleep(10) 
from databases import Database
from mqttClient import MqttClient
from dataProcessor import DataProcessor
from graphGenerator import GraphGenerator


#Cria um objeto da classe DAtabase
db = Database(host="localhost",user="user01",password="pi",database="monitoramento")

graphGenerator = GraphGenerator(db)
data_processor = DataProcessor(db)
mqtt_client = MqttClient("10.0.0.105",data_processor=data_processor)
graphGenerator.update_graph()


mqtt_client.start()







