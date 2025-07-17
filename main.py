import streamlit as st
from databases import Database
from mqttClient import MqttClient
from graphGenerator import GraphGenerator

# Cria conexão com o banco
db = Database(host="localhost", user="user01", password="pi", database="monitoramento")

# Criamos o MqttClient só para usar os botões de publish
mqtt_client = MqttClient("localhost")  # sem data_processor, não vai escutar nada

# Interface gráfica
graph = GraphGenerator(db, mqtt_client)
graph.update_graph()
graph.publish_button()