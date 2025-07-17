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
    def process_data(self, topic, payload):
        if topic == "monitoramento/temperatura":
            self.data_to_insert["monitoramento/temperatura"] = payload
        elif topic == "monitoramento/umidade":
            self.data_to_insert["monitoramento/umidade"] = payload

        temperatura = self.data_to_insert["monitoramento/temperatura"]
        umidade = self.data_to_insert["monitoramento/umidade"]

        if temperatura is not None and umidade is not None:
            if temperatura != self.previous_values["temperatura"] or umidade != self.previous_values["umidade"]:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.db.insert_into_database(temperatura, umidade, timestamp)
                self.previous_values["temperatura"] = temperatura
                self.previous_values["umidade"] = umidade

        if topic == "monitoramento/heartbeat":
            print(payload)
    