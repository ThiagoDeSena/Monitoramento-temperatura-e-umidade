import streamlit as st
from databases import Database
from mqttClient import MqttClient
from graphGenerator import GraphGenerator
from streamlit_autorefresh import st_autorefresh

# Configuração da página (Deve ser o primeiro comando)
st.set_page_config(page_title="Monitoramento Estufa", layout="wide")

# Cria conexão com o banco
db = Database(host="localhost", user="user01", password="pi", database="monitoramento")

# Criamos o MqttClient só para usar os botões de publish
mqtt_client = MqttClient("localhost")  # sem data_processor, não vai escutar nada

# Interface gráfica
graph = GraphGenerator(db, mqtt_client)
graph.update_graph()
graph.publish_button()

# 🔄 ATUALIZAÇÃO AUTOMÁTICA (Colocada ao final do script)
# interval=10000 significa 10 segundos. key é um identificador único.
st_autorefresh(interval=10000, limit=None, key="atualizador_estufa")