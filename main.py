import streamlit as st
from databases import Database
from mqttClient import MqttClient
from graphGenerator import GraphGenerator

# Configuração da página (DEVE ser o primeiro comando Streamlit do arquivo)
st.set_page_config(page_title="Monitoramento Estufa", layout="wide")

# 🔄 TIMER DE ATUALIZAÇÃO AUTOMÁTICA
# Esse fragmento roda silenciosamente a cada 10 segundos e força o script a reiniciar
@st.fragment(run_every=10)
def disparar_atualizacao_global():
    st.rerun()

disparar_atualizacao_global()

# Cria conexão com o banco
db = Database(host="localhost", user="user01", password="pi", database="monitoramento")

# Criamos o MqttClient só para usar os botões de publish
mqtt_client = MqttClient("localhost")  # sem data_processor, não vai escutar nada

# Interface gráfica
graph = GraphGenerator(db, mqtt_client)
graph.update_graph()
graph.publish_button()