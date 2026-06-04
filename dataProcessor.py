import datetime

class DataProcessor:
    def __init__(self, database):
        self.db = database
        self.current_values = {
            "temperatura": None,
            "umidade": None,
            "setpoint": None,
            "histerese": None
        }
        self.last_saved_values = {
            "temperatura": None,
            "umidade": None,
            "setpoint": None,
            "histerese": None
        }

    def process_data(self, topic, payload):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if topic == "monitoramento/temperatura":
            self.current_values["temperatura"] = payload

        elif topic == "monitoramento/umidade":
            self.current_values["umidade"] = payload

        elif topic == "monitoramento/setpoint":
            self.current_values["setpoint"] = payload
            # Salva setpoint imediatamente (não espera ter temperatura+umidade)
            if payload != self.last_saved_values["setpoint"]:
                try:
                    self.db.update_setpoint_histerese(setpoint=payload)
                    self.last_saved_values["setpoint"] = payload
                    print(f"[{now}] Setpoint atualizado: {payload}")
                except Exception as e:
                    print(f"[{now}] Erro ao atualizar setpoint: {e}")
            return

        elif topic == "monitoramento/histerese":
            self.current_values["histerese"] = payload
            # Salva histerese imediatamente (não espera ter temperatura+umidade)
            if payload != self.last_saved_values["histerese"]:
                try:
                    self.db.update_setpoint_histerese(histerese=payload)
                    self.last_saved_values["histerese"] = payload
                    print(f"[{now}] Histerese atualizada: {payload}")
                except Exception as e:
                    print(f"[{now}] Erro ao atualizar histerese: {e}")
            return

        elif topic == "monitoramento/heartbeat":
            print(f"[{now}] Heartbeat: {payload}")
            return  # nada a salvar

        temp = self.current_values["temperatura"]
        umid = self.current_values["umidade"]

        if temp is not None and umid is not None:
            if temp != self.last_saved_values["temperatura"] or umid != self.last_saved_values["umidade"]:
                try:
                    self.db.insert_into_database(temp, umid, now)
                    self.last_saved_values["temperatura"] = temp
                    self.last_saved_values["umidade"] = umid
                    print(f"[{now}] Dados salvos: T={temp}, U={umid}")
                except Exception as e:
                    print(f"[{now}] Erro ao inserir dados: {e}")
        else:
            print(f"[{now}] Aguardando dados válidos: T={temp}, U={umid}")
