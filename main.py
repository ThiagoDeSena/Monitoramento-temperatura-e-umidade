import time
time.sleep(10) 
from databases import Database
from mqttClient import MqttClient
from dataProcessor import DataProcessor
from graphGenerator import GraphGenerator

#Cria um objeto da classe DAtabase
db = Database(host="localhost",user="user01",password="pi",database="monitoramento")


data_processor = DataProcessor(db)
mqtt_client = MqttClient("10.0.0.115",data_processor=data_processor)
graphGenerator = GraphGenerator(db,mqtt_client)

graphGenerator.update_graph()
graphGenerator.publish_button()

import streamlit as st
#Garante que o loop do MQTT vai ser inicializado apenas uma vez
if "mqtt_started" not in st.session_state:
    print("Loop MQTT iniciado!")
    mqtt_client.start()
    st.session_state["mqtt_started"] = True

