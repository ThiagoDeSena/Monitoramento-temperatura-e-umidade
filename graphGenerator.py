import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


class GraphGenerator:
    
    def __init__(self,database):
        self.db = database

    # Consulta o banco de dados para obter todos dados
    @st.cache_data(ttl=30)  # Guarda os dados em um cache e Atualiza o cache a cada 30 segundos
    def fetch_all_data(_self):
        cursor = _self.db.conecao.cursor()  #Acesso o cursor do banco
        cursor.execute("SELECT temperatura, umidade, data FROM valores ORDER BY data DESC") # seleciona o 100 últimos valores de temperatura e data
        data = cursor.fetchall()    #Coloco os valores selecionados na variável 'data'
        #Cria um DataFrame a partir dos resultados da consulta
        df = pd.DataFrame(data, columns=['temperatura','umidade','data'])
        return df

    # Consulta o banco de dados para obter os dados das últimas 24 horas
    @st.cache_data(ttl=30)  # Guarda os dados em um cache e Atualiza o cache a cada 30 segundos
    def fetch_data_for_last_n_days(_self,num_days):
        end_data = datetime.now()
        start_date = end_data - timedelta(days=num_days)
        cursor = _self.db.conecao.cursor()  #Acesso o cursor do banco
        query = f"SELECT temperatura, umidade, data FROM valores WHERE data >= '{start_date:%Y-%m-%d %H:%M:%S}' ORDER BY data DESC" #Precisa usar o f antes para saber que ali dentro terá uma variável
        cursor.execute(query) # seleciona o 100 últimos valores de temperatura e data
        data = cursor.fetchall()    #Coloco os valores selecionados na variável 'data'
        #Cria um DataFrame a partir dos resultados da consulta
        df = pd.DataFrame(data, columns=['temperatura','umidade','data'])
        return df

    @st.cache_data(ttl=30) 
    def fetch_data_start_and_end(_self,start_date,end_date):
        cursor = _self.db.conecao.cursor()  #Acesso o cursor do banco
        query = f"SELECT temperatura, umidade, data FROM valores WHERE data BETWEEN '{start_date}' AND '{end_date}' ORDER BY data DESC" #Precisa usar o f antes para saber que ali dentro terá uma variável
        cursor.execute(query) # seleciona o 100 últimos valores de temperatura e data
        data = cursor.fetchall()    #Coloco os valores selecionados na variável 'data'
        #Cria um DataFrame a partir dos resultados da consulta
        df = pd.DataFrame(data, columns=['temperatura','umidade','data'])
        return df

    # Cria o gráfico
    def create_graph(self,data,variavel):

        #fig = px.line(data,x='data',y=['temperatura','umidade'],title='Evolução da temperatura e Umidade')
        fig = px.line(data,x='data',y=variavel)
        fig.update_traces(mode="markers+lines",hovertemplate=None) # Altera a visualização das informações no texto do mouser hover do gráfico
        fig.update_layout(
            hovermode="x unified",
            #hovertemplate="<br>Data:%{x}<br>Temperatura: %{y:.2f}ºC<br>Umidade: %{customdata:.2f}%"
        )
        st.plotly_chart(fig)
        #st.line_chart(data, x='data',y=['temperatura','umidade'])
        st.write("Última atualização: ",data['data'].max())

        # Atualiza o Gráfico
        if st.button('Atualizar Gráfico'):
            st.rerun()
      
    
    # Atualiza o gráfico com os valores novos
    def update_graph(self):
        
        print('Passou pelo update_graph')
        st.title("Gráfico de Monitoramento")
        df = self.fetch_data_for_last_n_days(1) #Por padrão já mostra 1 Dia
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

        self.create_graph(df,variavel)  




    

    