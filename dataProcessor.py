import datetime

class DataProcessor:
    def __init__(self,database):
        self.db = database
        self.data_to_insert = {
            "monitoramento/temperatura": None,
            "monitoramento/umidade": None
        }
        self.previous_values = {
            "temperatura": None,
            "umidade": None
        }

    # Verifica o tópico e insere o valor no banco de dados
    def process_data(self,topic,payload):
    
        self.data_to_insert[topic]=payload  # Atribui o dicionário daquele tópico a sua mensagem
    
        if self.data_to_insert["monitoramento/temperatura"] is not None and \
           self.data_to_insert["monitoramento/umidade"] is not None:
            temperatura = self.data_to_insert["monitoramento/temperatura"]
            umidade = self.data_to_insert["monitoramento/umidade"]

            #Verifica se os valores de temperatura ou umidade são diferentes dos valores anteriores para salvar no banco
            if temperatura != self.previous_values["temperatura"] or umidade != self.previous_values["umidade"]:
                timestamp = datetime.datetime.now()
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                self.db.insert_into_database(temperatura, umidade,timestamp_str)
                self.previous_values["temperatura"] = temperatura
                self.previous_values["umidade"] = umidade
    

        if topic == "monitoramento/heartbeat":
            print(payload)
    