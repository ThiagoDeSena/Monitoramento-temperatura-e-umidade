import paho.mqtt.client as mqtt
from dataProcessor import DataProcessor

class MqttClient:
    # Cria o cliente MQTT
    def __init__(self,broker_address, port=1883,keepalive=60,data_processor=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address,port,keepalive)
        self.data_processor = data_processor

    # Callback chamada quando a conexão com o broker é estabelecida
    def on_connect(self,client,userdata,flags,rc):

        if rc == 0:
            print("Conectado ao broker MQTT com sucesso!")

            #Increver-se nos tópicos desejados
            client.subscribe("monitoramento/temperatura")
            client.subscribe("monitoramento/umidade")
            client.subscribe("monitoramento/heartbeat")
        else:
            print(f"Falha ao conectar ao broker mqtt, código de retorno: {rc}")


    # Callback chamada quando uma nova mensagem é recebida.
    def on_message(self,client,userdata,msg):

        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        print(f"Mensagem recebida: tópico = {topic}, payload = {payload}")

        #   Aqui você pode chamar a função de processamento de dados, passando o tópico e o payload
        self.data_processor.process_data(topic,payload)

    #   Inicia o loop do cliente MQTT, aguardando por novas mensagens 
    def start(self):
        self.client.loop_forever()