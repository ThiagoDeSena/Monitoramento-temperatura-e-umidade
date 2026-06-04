import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


class GraphGenerator:
    
    def __init__(self,database,mqttClient):
        self.db = database
        self.mqtt_client = mqttClient

    def show_setpoint_histerese(self):
        """Exibe os valores atuais de setpoint e histerese de forma visual."""
        config = self.db.get_latest_setpoint_histerese()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if config["setpoint"] is not None:
                st.metric(
                    label="🎯 Setpoint",
                    value=f"{config['setpoint']:.1f}°C",
                    delta=None
                )
            else:
                st.metric(
                    label="🎯 Setpoint",
                    value="--",
                    delta=None
                )
        
        with col2:
            if config["histerese"] is not None:
                st.metric(
                    label="📊 Histerese",
                    value=f"{config['histerese']:.1f}°C",
                    delta=None
                )
            else:
                st.metric(
                    label="📊 Histerese",
                    value="--",
                    delta=None
                )
        
        with col3:
            # Criamos um rótulo menor usando markdown simulando o estilo do st.metric
            st.markdown("<small>⏰ Atualizado em</small>", unsafe_allow_html=True)
        
            if config["data_atualizacao"] is not None:
                # Se sua data for um objeto do banco, você pode formatá-la aqui se quiser, ex: config['data_atualizacao'].strftime('%d/%m/%Y %H:%M')
                st.write(f"🕒 {config['data_atualizacao'].strftime('%d/%m/%Y %H:%M')}")
            else:
                st.write("🕒 --")

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
    def create_graph(self, data, variavel):
        import plotly.graph_objects as go

        fig = go.Figure()

        if 'temperatura' in variavel:
            fig.add_trace(go.Scatter(
                x=data["data"],
                y=data["temperatura"],
                mode="lines+markers",
                name="🌡️ Temperatura (°C)",
                yaxis="y1",
                line=dict(color="red")
            ))

        if 'umidade' in variavel:
            fig.add_trace(go.Scatter(
                x=data["data"],
                y=data["umidade"],
                mode="lines+markers",
                name="💧 Umidade (%)",
                yaxis="y2",
                line=dict(color="blue")
            ))

        fig.update_layout(
            #title_text="Histórico de Temperatura e Umidade",
            #title_font=dict(size=20),
            margin=dict(t=70),  # margem superior maior para não sobrepor a legenda
            xaxis=dict(
                title="Data",
                showgrid=False,
                rangeslider=dict(visible=False),  # ✅ desativa o gráfico pequeno abaixo
                type="date"
            ),
            yaxis=dict(
                title="Temperatura (°C)",
                title_font=dict(color="red"),
                tickfont=dict(color="red")
            ),
            yaxis2=dict(
                title="Umidade (%)",
                title_font=dict(color="blue"),
                tickfont=dict(color="blue"),
                overlaying="y",
                side="right"
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="left", x=0),
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)


        if st.button("Atualizar Gráfico"):
            st.rerun()

      
    
    # # Atualiza o gráfico com os valores novos
    # def update_graph(self):
        
    #     print('Passou pelo update_graph')
    #     self.db.clean_duplicate_data_started()
    #     st.title("Gráfico de Monitoramento")
    #     df = self.fetch_data_for_last_n_days(1) #Por padrão já mostra 1 Dia
    #     self.show_latest_readings(df)
    #     #Botões para a seleção do intevalo
    #     with st.sidebar:
    #         st.header("Selecionar Período")
    #         col1,col2,col3 = st.columns(3)

    #         with col1:
    #             if st.button('1 Dia'):
    #                 df = self.fetch_data_for_last_n_days(1)

    #         with col2:
    #             if st.button('7 Dias'):
    #                 df = self.fetch_data_for_last_n_days(7)

    #         with col3:
    #             if st.button('30 Dias'):
    #                 df = self.fetch_data_for_last_n_days(30)

    #         if st.button('Tudo',use_container_width=True):
    #                 df = self.fetch_all_data()  #Pega os valores do dataframe criado na consulta do banco

    #         st.sidebar.expander('Selecionar Intervalo de Datas',icon=":material/search:")
    #         col1,col2 = st.columns(2)
    #         with col1:
    #             start_date = st.date_input("Data Inicial",datetime.today(),key="start")
    #         with col2:
    #             end_date = st.date_input("Data Final",datetime.today(),key="end")
    #         if st.button('Buscar',use_container_width=True):
    #             if start_date and end_date:
    #                 df = self.fetch_data_start_and_end(start_date,end_date)
    #             else:
    #                 st.warning('Selecione a data de inicil e fim da busca!',icon=":material/warning:")
        
    #         if df is not None:
    #             mask = df.columns != 'data' #Cria uma máscara com True para as colunas diferentes de data
    #             variavel = st.multiselect("Escolher variável",df.columns[mask],placeholder="Escolha uma opção")
    #             if not variavel:
    #                 variavel=['temperatura','umidade'] #Se não for escolhido nenhuma variável no st.multiselect então a minha variavel vai receber os dois valores ['temperatura','umidade']
    #         if self.mqtt_client.rele_ligado:
    #             st.success("Relé: Ligado")
    #         else:
    #             st.error("Relé: Desligado")  

    #     st.divider()  # separa o título da parte interativa de filtro 
    #     self.create_graph(df,variavel)  

    def update_graph(self):
        print('Passou pelo update_graph')
        self.db.clean_duplicate_data_started()
        st.title("Gráfico de Monitoramento")

        # Garante que o período escolhido sobrevive ao rerun
        if "periodo_dias" not in st.session_state:
            st.session_state.periodo_dias = 1
        if "df_custom" not in st.session_state:
            st.session_state.df_custom = None

        with st.sidebar:
            st.header("Selecionar Período")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button('1 Dia'):
                    st.session_state.periodo_dias = 1
                    st.session_state.df_custom = None
            with col2:
                if st.button('7 Dias'):
                    st.session_state.periodo_dias = 7
                    st.session_state.df_custom = None
            with col3:
                if st.button('30 Dias'):
                    st.session_state.periodo_dias = 30
                    st.session_state.df_custom = None

            if st.button('Tudo', use_container_width=True):
                st.session_state.periodo_dias = None
                st.session_state.df_custom = None

            st.sidebar.expander('Selecionar Intervalo de Datas', icon=":material/search:")
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Data Inicial", datetime.today(), key="start")
            with col2:
                end_date = st.date_input("Data Final", datetime.today(), key="end")

            if st.button('Buscar', use_container_width=True):
                if start_date and end_date:
                    st.session_state.df_custom = self.fetch_data_start_and_end(start_date, end_date)
                    st.session_state.periodo_dias = None
                else:
                    st.warning('Selecione a data inicial e fim da busca!', icon=":material/warning:")

            # Busca os dados conforme o estado salvo
            if st.session_state.df_custom is not None:
                df = st.session_state.df_custom
            elif st.session_state.periodo_dias is not None:
                df = self.fetch_data_for_last_n_days(st.session_state.periodo_dias)
            else:
                df = self.fetch_all_data()

            if df is not None:
                mask = df.columns != 'data'
                variavel = st.multiselect("Escolher variável", df.columns[mask], placeholder="Escolha uma opção")
                if not variavel:
                    variavel = ['temperatura', 'umidade']

            if self.mqtt_client.rele_ligado:
                st.success("Relé: Ligado")
            else:
                st.error("Relé: Desligado")

        self.show_latest_readings(df)
        st.divider()
        self.create_graph(df, variavel)

    # Publica uma mensagem para acionar o relé
    def publish_button(self):
        with st.sidebar:
            st.divider()
            st.subheader("🔧 Configurar Controle")

            # Entradas numéricas com valores padrão e limites
            setpoint = st.number_input("🌡️ Setpoint de Temperatura (°C)", min_value=0.0, max_value=100.0, value=40.0, step=0.5)
            histerese = st.number_input("🔁 Histerese (°C)", min_value=0.0, max_value=20.0, value=2.0, step=0.1)

            if st.button("✅ Enviar Setpoint/Histerese", use_container_width=True):
                try:
                    self.mqtt_client.publish_message("monitoramento/setpoint", str(setpoint))
                    self.mqtt_client.publish_message("monitoramento/histerese", str(histerese))
                    st.success(f"Setpoint ({setpoint} °C) e Histerese ({histerese} °C) enviados com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao enviar: {e}")

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
            data_formatada = data.strftime('%d/%m/%Y %H:%M')
            st.write(f"🕒 {data_formatada}")
        
        # Mostra setpoint e histerese logo abaixo
        st.subheader("⚙️ Configurações Atuais")
        self.show_setpoint_histerese()
        