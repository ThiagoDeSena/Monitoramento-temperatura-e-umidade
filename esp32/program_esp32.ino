#include <WiFi.h>
#include <PubSubClient.h> //comunicação com um servidor MQTT
#include "DHT.h"
#include <TimeLib.h>  // Biblioteca para manipulação de datas e horas
#include <NTPClient.h>
#include <WiFiUdp.h>

const char* ssid = "ifce-espacoMaker";
const char* password = "CR1AT1V1UM";
// const char* mqtt_server = "broker.hivemq.com"; //endereço do servidor MQTT online
//const char* mqtt_server = "10.0.0.105"; //endereço do Raspberry
const char* mqtt_server = "10.0.0.108"; //endereço do Raspberry

WiFiClient espClient; //objeto para gerenciar a conexão Wi-Fi.
PubSubClient client(espClient); //objeto para se conectar ao servidor MQTT, utilizando a conexão Wi-Fi 

WiFiUDP ntpUDP;
const int timeZone = -3; // Ajuste para o seu fuso horário
const char* ntpServer = "pool.ntp.org";
const unsigned long gmtOffset = 3600 * timeZone;
const unsigned int updateInterval = 60000; // Atualiza a hora a cada minuto

NTPClient timeClient(ntpUDP,ntpServer,gmtOffset,updateInterval); //Pega a hora e data atual


//unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50) //tamanho máximo de uma mensagem que pode ser enviada ou recebida.
char msg[MSG_BUFFER_SIZE]; //array de caracteres que será usado para armazenar as mensagens.

#define BUZZER_PIN 18
#define DHTPIN 13 // pino DHT11
#define DHTTYPE DHT11 // DHT 11
#define RELE 2
bool releLigado = false; // Estado do relé

// Variáveis para armazenar os últimos valores lidos de temperatura e umidade
float humidadeAnterior=0,temperaturaAnterior=0; 
// Variáveis para armazenar o tempo do último envio da umidade e temperatura e da minha mensagem de funcionamento da aplicação MQTT
static unsigned long tempoUltimoEnvioUmidade = 0, tempoUltimoEnvioTemperatura = 0, tempoUltimoHeartbeat  = 0;
const long intervalo = 300000;  // Intervalo de 5 minutos em milissegundos

DHT dht(DHTPIN, DHTTYPE);

//Toda vez que uma nova mensagem chega no tópico que o ESP32 está "ouvindo", essa função é automaticamente chamada
void callback(char* nomeDoTopico, byte* dadosEnviados, unsigned int tamanhoDoConteudoDaMensagem){
  Serial.print("Message arrived [");
  Serial.print(nomeDoTopico);
  Serial.print("] ");
  for (int i=0; i<tamanhoDoConteudoDaMensagem; i++) {
    Serial.print((char)dadosEnviados[i]);
  }
  Serial.println();

  if((char)dadosEnviados[0]=='L' || (char)dadosEnviados[0]=='l'){
    digitalWrite(RELE, HIGH);
    snprintf(msg, MSG_BUFFER_SIZE, "O RELE está acesso");
    Serial.print("Publica mensagem: ");
    Serial.println(msg);
    client.publish("monitoramento/led",msg);
  }

  if ((char)dadosEnviados[0]=='D' || (char)dadosEnviados[0]=='d') {
    digitalWrite(RELE, LOW);
    snprintf(msg, MSG_BUFFER_SIZE, "O RELE está apagado");
    Serial.print("Publica mensagem: ");
    Serial.println(msg);
    client.publish("monitoramento/led",msg);
  }

  if ((char)dadosEnviados[0]=='A' || (char)dadosEnviados[0]=='a') {
    digitalWrite(BUZZER_PIN, HIGH);
    snprintf(msg, MSG_BUFFER_SIZE, "A sirene está Ligada");
    Serial.print("Publica mensagem: ");
    Serial.println(msg);
    client.publish("monitoramento/sirene",msg);
  }

  if ((char)dadosEnviados[0]=='P' || (char)dadosEnviados[0]=='p') {
    digitalWrite(BUZZER_PIN, LOW);
    snprintf(msg, MSG_BUFFER_SIZE, "A sirene está Desligada");
    Serial.print("Publica mensagem: ");
    Serial.println(msg);
    client.publish("monitoramento/sirene",msg);
  }

}

// Setup da conecção wifi
void setup_wifi(){
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

// Reconecção ao Broker MQTT
void reconnect(){
  while(!client.connected()){
    Serial.print("Attempting MQTT connection...");

    String clientId = "ENGEASIER_MQTT";
    clientId += String(random(0xffff),HEX);

    if(client.connect(clientId.c_str())){
      Serial.println("Conectado");

      client.subscribe("monitoramento/publisher");
    }else{
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }

}

void controleTemperatura(float temperatura,float humidade){

  if (temperatura >= 50 && !releLigado) {
    digitalWrite(RELE, HIGH); // Liga o relé
    releLigado = true;
    Serial.println("Relé ligado: Temperatura >= 50°C");
    client.publish("monitoramento/rele", "Ligado"); // Publica no MQTT
  }
  else if (temperatura < 40 && releLigado) {
    digitalWrite(RELE, LOW); // Desliga o relé
    releLigado = false;
    Serial.println("Relé desligado: Temperatura < 40°C");
    client.publish("monitoramento/rele", "Desligado"); // Publica no MQTT
  }

}

void dht11(){
  unsigned long tempoAtual = millis();  //Armazena o tempo atual

  float humidade = dht.readHumidity(); //Ler a humidade
  float temperatura = dht.readTemperature(); //Ler a temperatura
  
  controleTemperatura(temperatura,humidade);
  // testa se retorno é valido, caso contrário algo está errado.
  if (isnan(temperatura) || isnan(humidade)) 
  {
    char* mensagem = "Failed to read from DHT";
    Serial.println(mensagem);
    sprintf(msg, "%s", mensagem);
    client.publish("monitoramento/temperatura",mensagem);
    client.publish("monitoramento/umidade",mensagem);
  }
  else
  {
    // Envia a mensagem se a umidade lida for diferente que a anterior ou se já tiver passado 5min do último envio
    if(humidade != humidadeAnterior || tempoAtual - tempoUltimoEnvioUmidade >= intervalo){
      humidadeAnterior = humidade;
      Serial.print("Umidade: ");
      Serial.print(humidade);
      Serial.println(F(" °%"));
      sprintf(msg,"%.2f",humidade);
      client.publish("monitoramento/umidade",msg);
      tempoUltimoEnvioUmidade = tempoAtual;
    }

    // Envia a mensagem se a temperatura lida for diferente que a anterior ou se já tiver passado 5min do último envio
    if(temperatura != temperaturaAnterior || tempoAtual - tempoUltimoEnvioTemperatura >= intervalo){
      temperaturaAnterior = temperatura;
      Serial.print("Temperatura: ");
      Serial.print(temperatura);
      Serial.println((" °C"));
      sprintf(msg,"%.2f",temperatura);
      client.publish("monitoramento/temperatura",msg);
      tempoUltimoEnvioTemperatura = tempoAtual;
    }
    
  }
}

//Confirma que a aplicação MQTT está funcionando corretamente(Batimento cardiaco a cada 2 min)
void heartbeat(){


  timeClient.update();
  setTime(timeClient.getEpochTime()); //Sincronizar a Hora

  unsigned long tempoAtual = millis();
  const unsigned long intervaloHeartbeat = 60000; // 2 minutos em milissegundos

  if(tempoAtual - tempoUltimoHeartbeat >= intervaloHeartbeat){
    // Obtém a hora atual
    int horaAtual = hour();
    int minutoAtual = minute();
    int segundoAtual = second();
    int diaAtual = day();
    int mesAtual = month();
    int anoAtual = year();
      
    // Formata a data e hora
    char dataHora[32];
    sprintf(dataHora, "%02d/%02d/%04d %02d:%02d:%02d", diaAtual,mesAtual,anoAtual, horaAtual, minutoAtual, segundoAtual);

    // Concatena a data e hora à mensagem do heartbeat
    char mensagemHeartbeat[64];
    sprintf(mensagemHeartbeat, dataHora);

    Serial.println(mensagemHeartbeat);
    client.publish("monitoramento/heartbeat",mensagemHeartbeat);
    tempoUltimoHeartbeat = tempoAtual;
  }
}

void setup() {
  // put your setup code here, to run once:

  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, LOW);
  pinMode(BUZZER_PIN, OUTPUT);
  dht.begin(); //Inicializa o DHT11

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server,1883);
  client.setCallback(callback);
  timeClient.begin();

  

}

boolean i = false;
void loop() {
  
  dht11();
  heartbeat();

  if(!client.connected()){
    reconnect();
  }

  if(!i){
    // Publica o estado inicial do relé no MQTT
    client.publish("monitoramento/rele",  releLigado ? "Ligado" : "Desligado");
    i = true;
  }

  

  client.loop();
}
