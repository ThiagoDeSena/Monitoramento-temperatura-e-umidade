import time
import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, broker_address, port=1883, keepalive=60, data_processor=None):
        """
        Inicializa o cliente MQTT, define callbacks e conecta ao broker.
        """
        self.broker_address = broker_address
        self.port = port
        self.keepalive = keepalive
        self.data_processor = data_processor
        self.rele_ligado = False
        self.topics = [
            "monitoramento/temperatura",
            "monitoramento/umidade",
            "monitoramento/heartbeat",
            "monitoramento/rele"
        ]

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.connect()

    def connect(self):
        """
        Tenta conectar ao broker MQTT pela primeira vez.
        Se falhar, chama retry_connection() para tentar novamente.
        """
        try:
            self.client.connect(self.broker_address, self.port, self.keepalive)
            print("[MQTT] Conectando ao broker...")
        except Exception as e:
            print(f"[MQTT] Erro ao conectar: {e}")
            self.retry_connection()

    def retry_connection(self):
        """
        Tenta reconectar ao broker indefinidamente a cada 5 segundos em caso de falha.
        """
        while True:
            try:
                print("[MQTT] Tentando reconectar ao broker...")
                self.client.reconnect()
                print("[MQTT] Reconectado com sucesso!")
                break
            except Exception as e:
                print(f"[MQTT] Falha na reconexão: {e}")
                time.sleep(5)

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback chamada quando o cliente conecta ao broker.
        Realiza a inscrição em todos os tópicos relevantes.
        """
        if rc == 0:
            print("[MQTT] Conectado ao broker com sucesso!")
            for topic in self.topics:
                client.subscribe(topic)
                print(f"[MQTT] Inscrito no tópico: {topic}")
        else:
            print(f"[MQTT] Falha na conexão, código: {rc}")

    def on_disconnect(self, client, userdata, rc):
        """
        Callback chamada quando o cliente é desconectado.
        Tenta reconectar e reinscreve os tópicos.
        """
        print(f"[MQTT] Desconectado! Código: {rc}")
        if rc != 0:
            self.retry_connection()
            for topic in self.topics:
                client.subscribe(topic)
                print(f"[MQTT] Reinscrito no tópico: {topic}")

    def on_message(self, client, userdata, msg):
        """
        Callback chamada quando uma mensagem é recebida.
        Processa o payload e envia para o DataProcessor.
        """
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        print(f"[MQTT] Mensagem recebida - Tópico: {topic} | Payload: {payload}")

        if topic == "monitoramento/rele":
            self.rele_state(payload)

        if self.data_processor:
            try:
                self.data_processor.process_data(topic, payload)
            except Exception as e:
                print(f"[MQTT] Erro no processador de dados: {e}")

    def on_publish(self, client, userdata, mid):
        """
        Callback chamada quando uma mensagem é publicada com sucesso.
        """
        print(f"[MQTT] Mensagem publicada com sucesso! mid={mid}")

    def publish_message(self, topic, message):
        """
        Publica uma mensagem em um tópico MQTT e verifica se foi bem-sucedida.
        """
        try:
            result = self.client.publish(topic, message)
            status = result[0]
            if status == mqtt.MQTT_ERR_SUCCESS:
                print(f"[MQTT] Mensagem publicada no tópico '{topic}': {message}")
            else:
                print(f"[MQTT] Falha ao publicar no tópico '{topic}'")
        except Exception as e:
            print(f"[MQTT] Erro ao publicar mensagem: {e}")

    def rele_state(self, payload):
        """
        Atualiza o estado do relé com base na mensagem recebida.
        """
        self.rele_ligado = payload.lower() == "ligado"

    def start(self):
        """
        Inicia o loop MQTT em segundo plano (modo não bloqueante).
        """
        self.client.loop_start()
