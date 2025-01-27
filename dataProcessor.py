
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
           self.data_to_insert["monitoramento/umidade"] is not None and \
           (self.data_to_insert["monitoramento/temperatura"] != self.previous_values["temperatura"] or
            self.data_to_insert["monitoramento/umidade"] != self.previous_values["umidade"]):
            temperatura = self.data_to_insert["monitoramento/temperatura"]
            umidade = self.data_to_insert["monitoramento/umidade"]
            self.db.insert_into_database(temperatura, umidade)
            self.previous_values["temperatura"] = temperatura
            self.previous_values["umidade"] = umidade

        if topic == "monitoramento/heartbeat":
            print(payload)
    