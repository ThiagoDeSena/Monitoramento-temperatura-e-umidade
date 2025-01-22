import time
time.sleep(3) 

import paho.mqtt.client as mqtt
import mariadb
import sys
import datetime
import pandas as pd 
import streamlit as st


try:
    conecao = mariadb.connect(
        user="user01",  #usuário criado no mariaDB
        password="pi",  #Senha Criada no mariaDB para o usuário 'user01'
        host="localhost", #host criado no mariadb para o usuário 'user01'
        database="monitoramento"    #Nome do banco de teste criado no mariaDB
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

cursor = conecao.cursor()
dados ={"temperatura":None,"umidade":None}
ultima_temperatura = 0
ultima_umidade = 0
ultima_insercao = time.time()   #Hora atual

def inserir_valores(temperatura,umidade):
    cursor.execute("INSERT INTO valores (temperatura,umidade) VALUES (?,?)",(temperatura,umidade)) ##Insere os valores de "temperatura" e "umidade" na tabela 'valores' do banco de dados


def receber_mensagem(cliente,userdata,message):
    topico = message.topic #Valor do tópico que o raspberry se inscreveu
    valor = str(message.payload.decode("utf-8"))
    
    if topico == "monitoramento/temperatura":
        dados["temperatura"] = valor
    elif topico == "monitoramento/umidade":
        dados["umidade"] = valor
    
    
    if dados["temperatura"] is not None and dados["umidade"] is not None:
        tempo = datetime.datetime.now()
        print(f"Temperatura: {dados['temperatura']} ºC , Humidade: {dados['umidade']}%, Data: {tempo}")

        global ultima_temperatura
        global ultima_umidade
        global ultima_insercao

        if ultima_temperatura != dados["temperatura"] or ultima_umidade!=dados["umidade"] or time.time() - ultima_insercao >=300: # time.time() - ultima_insercao >=300 -> Se a diferença entre o tempo atual e o tempo da última temperatura for maior que 5 min
            inserir_valores(dados['temperatura'],dados['umidade'])
            conecao.commit() ##Salva as alterações feitas no banco de dados
            ultima_temperatura = dados["temperatura"]
            ultima_umidade = dados["umidade"]
            ultima_insercao = time.time()   #Recebe a hora atual em que foi inserido valores no banco
    
    criar_grafico()


valoresTemperatura = []
valoresData = []

def criar_grafico():
    cursor.execute("SELECT * FROM valores;") # O cursos selecionou todos os dados da tabela 'valores'
    valores = cursor.fetchall() # Extrair todos os registros retornados de uma consulta SQL e armazena na variável valores
    
    if valores:
        for coluna in  valores:
            valoresTemperatura.append(coluna[1])
            valoresData.append(coluna[3])
    else:
        print("Nenhum valor encontrado!")

    #Cria um DataFrame
    dataFrame = pd.DataFrame({'Temperatura':valoresTemperatura, 'Data':valoresData})

    #Apaga o index do dataFrame
    dataFrame = dataFrame.reset_index(drop=True)

    #markdown
    st.write("""
    # Gráfico de Temperatura e Humidade
    Monitoramento da Temperatura da Estufa
    """)

    print('TIPO DE DADOS:')
    print(dataFrame.dtypes)

    st.line_chart(dataFrame, x='Data',y = 'Temperatura')

    st.write("""
    # Fim do App
    """)



cliente = mqtt.Client()
conexao = cliente.connect(host="10.0.0.105") 
#10.0.0.105 
#mqtt-dashboard.com

#cliente.loop_start()
cliente.subscribe("monitoramento/temperatura")
cliente.subscribe("monitoramento/umidade")


cliente.on_message = receber_mensagem

cliente.loop_forever()



print(f"Last Inserted ID: {cursor.lastrowid}")
cursor.close()
conecao.close()

while True:
    pass

   