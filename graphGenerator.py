import streamlit as st
import pandas as pd
import plotly.express as px


class GraphGenerator:
    
    def __init__(self,database):
        self.db = database

    # Consulta o banco de dados para obter os últimos dados
    @st.cache_data(ttl=30)  # Guarda os dados em um cache e Atualiza o cache a cada 30 segundos
    def fetch_data(_self):
        cursor = _self.db.conecao.cursor()  #Acesso o cursor do banco
        cursor.execute("SELECT temperatura, umidade, data FROM valores ORDER BY data DESC LIMIT 500") # seleciona o 100 últimos valores de temperatura e data
        data = cursor.fetchall()    #Coloco os valores selecionados na variável 'data'

        #Cria um DataFrame a partir dos resultados da consulta
        df = pd.DataFrame(data, columns=['temperatura','umidade','data'])
        

        return df


    # Cria o gráfico
    def create_graph(self,data):

        st.title("Gráfico de Temperatura")

        fig = px.line(data,x='data',y=['temperatura','umidade'],title='Evolução da temperatura e Umidade')
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
        df = self.fetch_data()  #Pega os valores do dataframe criado na consulta do banco
        self.create_graph(df)

    '''def create_graph(self,data):
        if 'fig' not in st.session_state:
            #Cria o gráfico pela 1° vez
            fig = px.line(data, x='data',y='temperatura')
            st.plotly_chart(fig, use_container_width=True)
            st.session_state.fig = fig
        else:
            #Atualiza o gráfico existente
            fig = st.session_state.fig
            fig.add_trace(go.Scatter(x=data['data'],y=data['temperatura'],name='Nova LInha'))
            st.plotly_chart(fig)'''

    

    