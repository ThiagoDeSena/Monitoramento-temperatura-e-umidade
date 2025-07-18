import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


class GraphGenerator:
    
    def __init__(self,database,mqttClient):
        self.db = database
        self.mqtt_client = mqttClient

    def run_query(self, query):
        """Executa uma consulta SQL e retorna um DataFrame."""
        try:
            self.db.reconnect_if_needed()
            cursor = self.db.conexao.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=["temperatura", "umidade", "data"])
        except Exception as e:
            st.error(f"Erro ao executar consulta: {e}")
            return pd.DataFrame(columns=["temperatura", "umidade", "data"])
        

    # Consulta o banco de dados para obter todos dados
    def fetch_all_data(self):
        query = "SELECT temperatura, umidade, data FROM valores ORDER BY data DESC" # seleciona o 100 últimos valores de temperatura e data
        return self.run_query(query)

    # Consulta o banco de dados para obter os dados das últimas 24 horas
    def fetch_data_for_last_n_days(self,num_days):
        end_data = datetime.now()
        start_date = end_data - timedelta(days=num_days)
        query = f"SELECT temperatura, umidade, data FROM valores WHERE data >= '{start_date:%Y-%m-%d %H:%M:%S}' ORDER BY data DESC" #Precisa usar o f antes para saber que ali dentro terá uma variável
        return self.run_query(query)

    # Consulta os valores selecionados entre datas que o usuário selecionou
    def fetch_data_start_and_end(self,start_date,end_date):
        query = f"SELECT temperatura, umidade, data FROM valores WHERE data >= '{start_date} 00:00:00' AND data <= '{end_date} 23:59:59' ORDER BY data DESC" #Precisa usar o f antes para saber que ali dentro terá uma variável
        return self.run_query(query)

    # Cria o gráfico
    def create_graph(self,data,variavel):

        fig = px.line(data,x='data',y=variavel)
        fig.update_traces(mode="markers+lines",hovertemplate=None) # Altera a visualização das informações no texto do mouser hover do gráfico
        fig.update_layout(
            hovermode="x unified",
        )
        st.plotly_chart(fig)

        # Atualiza o Gráfico
        if st.button('Atualizar Gráfico'):
            st.rerun()
      
    
    # Atualiza o gráfico com os valores novos
    def update_graph(self):
        
        print('Passou pelo update_graph')
        self.db.clean_duplicate_data_started()
        st.title("Gráfico de Monitoramento")
        df = self.fetch_data_for_last_n_days(1) #Por padrão já mostra 1 Dia
        self.show_latest_readings(df)
        #Botões para a seleção do intevalo
        with st.sidebar:
            st.header("Selecionar Período")
            col1,col2,col3 = st.columns(3)

            with col1:
                if st.button('1 Dia'):
                    df = self.fetch_data_for_last_n_days(1)

            with col2:
                if st.button('7 Dias'):
                    df = self.fetch_data_for_last_n_days(7)

            with col3:
                if st.button('30 Dias'):
                    df = self.fetch_data_for_last_n_days(30)

            if st.button('Tudo',use_container_width=True):
                    df = self.fetch_all_data()  #Pega os valores do dataframe criado na consulta do banco

            st.sidebar.expander('Selecionar Intervalo de Datas',icon=":material/search:")
            col1,col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Data Inicial",datetime.today(),key="start")
            with col2:
                end_date = st.date_input("Data Final",datetime.today(),key="end")
            if st.button('Buscar',use_container_width=True):
                if start_date and end_date:
                    df = self.fetch_data_start_and_end(start_date,end_date)
                else:
                    st.warning('Selecione a data de inicil e fim da busca!',icon=":material/warning:")
        
            if df is not None:
                mask = df.columns != 'data' #Cria uma máscara com True para as colunas diferentes de data
                variavel = st.multiselect("Escolher variável",df.columns[mask],placeholder="Escolha uma opção")
                if not variavel:
                    variavel=['temperatura','umidade'] #Se não for escolhido nenhuma variável no st.multiselect então a minha variavel vai receber os dois valores ['temperatura','umidade']
            if self.mqtt_client.rele_ligado:
                st.success("Relé: Ligado")
            else:
                st.error("Relé: Desligado")  

        st.divider()  # separa o título da parte interativa de filtro
        self.create_graph(df,variavel)  


    # Publica uma mensagem para acionar o relé
    def publish_button(self):
        with st.sidebar:
            st.divider()  # Separador visual
            st.subheader("Enviar mensagem")

            col1, col2 = st.columns(2)
            
            with col1:
                st.button(
                    'Acionar Buzzer',
                    on_click=self.publish_message_callback,
                    args=("a",),
                    use_container_width=True
                )
                st.button(
                    'Acionar Relé',
                    on_click=self.publish_message_callback,
                    args=("l",),
                    use_container_width=True
                )
            
            with col2:
                st.button(
                    'Desaciona Buzzer',
                    on_click=self.publish_message_callback,
                    args=("p",),
                    use_container_width=True
                )
                st.button(
                    'Desaciona Relé',
                    on_click=self.publish_message_callback,
                    args=("d",),
                    use_container_width=True
                )

                    

    
    #Método de Callback para não reinicializar a página
    def publish_message_callback(self,message):
        self.mqtt_client.publish_message("monitoramento/publisher",message)
    
    def show_latest_readings(self, df):
        """Exibe as últimas leituras de temperatura e umidade em destaque."""
        if df.empty:
            st.warning("Nenhum dado disponível para exibir.")
            return

        latest = df.iloc[0]
        temperatura = latest["temperatura"]
        umidade = latest["umidade"]
        data = latest["data"]

        st.divider()
        st.subheader("📊 Última Leitura")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌡️ Temperatura (°C)", f"{temperatura}")
        with col2:
            st.metric("💧 Umidade (%)", f"{umidade}")
        with col3:
            st.write(f"🕒 {data}")
