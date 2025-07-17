import paho.mqtt.client as mqtt
from dataProcessor import DataProcessor

class MqttClient:
    # Cria o cliente MQTT
    def __init__(self,broker_address, port=1883,keepalive=60,data_processor=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(broker_address,port,keepalive)
        self.data_processor = data_processor
        self.rele_ligado = False #Inicializa o estado do relé como desligado

    # Callback chamada quando a conexão com o broker é estabelecida
    def on_connect(self,client,userdata,flags,rc):

        if rc == 0:
            print("Conectado ao broker MQTT com sucesso!")

            #Increver-se nos tópicos desejados
            client.subscribe("monitoramento/temperatura")
            client.subscribe("monitoramento/umidade")
            client.subscribe("monitoramento/heartbeat")
            client.subscribe("monitoramento/rele")
        else:
            print(f"Falha ao conectar ao broker mqtt, código de retorno: {rc}")


    # Callback chamada quando uma nova mensagem é recebida.
    def on_message(self,client,userdata,msg):

        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        print(f"Mensagem recebida: tópico = {topic}, payload = {payload}")

        if topic == "monitoramento/rele":
            self.rele_state(payload)

        #   Aqui você pode chamar a função de processamento de dados, passando o tópico e o payload
        if self.data_processor:
            self.data_processor.process_data(topic,payload)
    
    def rele_state(self,payload):
        if payload.lower() == "ligado":
            self.rele_ligado = True
        elif payload.lower() == "desligado":
            self.rele_ligado = False

    #   Inicia o loop do cliente MQTT, aguardando por novas mensagens 
    def start(self):
        #self.client.loop_forever()
        self.client.loop_start() # Inicia o loop MQTT em uma thread separada e não bloqueia o resto da aplicação

    #Publica uma messagem no topico passado
    def publish_message(self,topic,message):
        self.client.publish(topic,message)
        print(f"Messagem publicada no tópico {topic}: {message}")

    
    def on_disconnect(self, client, userdata, rc):
        print(f"[MQTT] Desconectado do broker! Código rc = {rc}")
        if rc != 0:
            while True:
                try:
                    print("[MQTT] Tentando reconectar...")
                    client.reconnect()
                    print("[MQTT] Reconectado com sucesso!")
                    break
                except Exception as e:
                    print(f"[MQTT] Erro ao tentar reconectar: {e}")
                    time.sleep(5)  # espera 5 segundos antes de tentar de novo