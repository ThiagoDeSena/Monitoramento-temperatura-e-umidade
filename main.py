import streamlit as st
from streamlit_autorefresh import st_autorefresh
from databases import Database
from mqttClient import MqttClient
from graphGenerator import GraphGenerator


# 1. Configuração da página — SEMPRE primeiro
st.set_page_config(page_title="Monitoramento Estufa", layout="wide")

# 2. Autorefresh — SEMPRE logo após set_page_config
st_autorefresh(interval=10000, limit=None, key="atualizador_estufa")

# 3. Inicializa objetos UMA VEZ usando session_state
# Sem isso, a cada rerun o Streamlit recria tudo do zero
if "db" not in st.session_state:
    st.session_state.db = Database(
        host="localhost", user="user01", password="pi", database="monitoramento"
    )

if "mqtt_client" not in st.session_state:
    st.session_state.mqtt_client = MqttClient("localhost")

# 4. Recupera os objetos do session_state
db = st.session_state.db
mqtt_client = st.session_state.mqtt_client

# Interface gráfica
graph = GraphGenerator(db, mqtt_client)

try:
    graph.update_graph()
except Exception as e:
    st.error(f"Erro no update_graph: {e}")
    st.exception(e)  # Mostra o traceback completo na tela

try:
    graph.publish_button()
except Exception as e:
    st.error(f"Erro no publish_button: {e}")
    st.exception(e)
