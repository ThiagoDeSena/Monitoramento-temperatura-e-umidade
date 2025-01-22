import streamlit as st
import pandas as pd


class GraphGenerator:
    
    def __init__(self,database):
        self.db = database

    # Consulta o banco de dados para obter os últimos dados
    @st.cache_data(ttl=30)  # Guarda os dados em um cache e Atualiza o cache a cada 30 segundos
    def fetch_data(_self):
        cursor = _self.db.conecao.cursor()
        cursor.execute("SELECT temperatura,data FROM valores ORDER BY data DESC LIMIT 100")
        data = cursor.fetchall()

        #Cria um DataFrame a partir dos resultados da consulta
        df = pd.DataFrame(data, columns=['temperatura','data'])

        return df

    # Cria o gráfico
    def create_graph(self,data):

        st.title("Gráfico de Temperatura")
        st.line_chart(data, x='data',y='temperatura')
        st.write("Última atualização: ",data['data'].max())
        

    # Atualiza o gráfico com os valores novos
    def update_graph(self):
        df = self.fetch_data()
        self.create_graph(df)

    