# Projeto: Estufa *In Situ* com IoT para Conservação de Filamentos de PLA

![20250718_145217(2)](https://github.com/user-attachments/assets/162769d0-29eb-46ba-a0fd-8e173c12d440)

## 📌 Descrição do Projeto

Este projeto desenvolve um sistema de aquecimento e monitoramento *in situ* para a conservação de filamentos de PLA utilizados em impressão 3D. A solução proposta substitui estufas comerciais caras, oferecendo um controle local e automatizado de temperatura e umidade, com monitoramento em tempo real via IoT, garantindo maior vida útil e qualidade do material.

---

## 🎯 Objetivo

Criar um kit de aquecimento de baixo custo que possa ser instalado diretamente no local de armazenamento dos filamentos, integrado a um sistema IoT para monitoramento contínuo de temperatura e umidade, evitando a degradação por hidrólise do PLA.

---
<img width="1919" height="881" alt="image" src="https://github.com/user-attachments/assets/62e6f9f4-3c50-4f16-b58b-3ba4adea2a21" />

## ⚙️ Funcionamento do Sistema

### Componentes Principais

- **Sensor DHT11**: Mede temperatura e umidade no interior do armário.
- **Microcontrolador ESP32** (embarcado na placa Kincony KC868-A4): Processa os dados do sensor e envia via protocolo MQTT.
- **Raspberry Pi 4**: Atua como *broker* MQTT (Mosquitto) e servidor de aplicação.
- **Banco de Dados MariaDB**: Armazena os dados coletados.
- **Placa de Aquecimento (120W)**: Aquece o ambiente quando a temperatura está abaixo do *setpoint*.
- **Ventilador**: Auxilia na circulação do ar aquecido.
- **Fonte de 12V**: Alimenta o sistema.

### Fluxo de Dados

1. O **DHT11** coleta temperatura e umidade.
2. O **ESP32** envia os dados para o **Raspberry Pi 4** via **MQTT**.
3. Um script em **Python** no Raspberry Pi processa e armazena os dados no **MariaDB**.
4. Um *dashboard* interativo, desenvolvido com **Streamlit**, exibe os dados em tempo real.
5. O **Ngrok** permite acesso remoto ao *dashboard* via internet.

### Controle de Aquecimento

- **Liga** a placa de aquecimento quando a temperatura < 32°C.
- **Desliga** quando a temperatura > 40°C.
- Mantém a umidade relativa em torno de **42%**, contra ~62% sem aquecimento.

---

## 📊 Resultados Obtidos

- Redução de **>20%** na umidade relativa.
- Temperatura mantida entre **32°C e 40°C**.
- Consumo energético eficiente: **~36% da potência total** em ciclo contínuo.
- Filamentos preservados sem sinais de fragilidade ou hidrólise.

---

## 💰 Custo do Projeto (Março/2025)

| Componente            | Preço (R$)  |
|-----------------------|-------------|
| Fonte 12V             | 22,99       |
| Ventilador            | 5,99        |
| Placa Kincony KC868-A4| 221,18      |
| Sensor DHT11          | 8,45        |
| Raspberry Pi 4 (4GB)  | 490,00      |
| **Total**             | **R$ 748,61** |

> 💡 **Vantagem financeira**: Cerca de **R$ 1.500,00** mais barato que uma estufa comercial similar.

---

## 🛠️ Como Reproduzir o Projeto

### Materiais Necessários

- Placa Kincony KC868-A4 com ESP32
- Sensor DHT11
- Raspberry Pi 4
- Placa de aquecimento (120W)
- Ventilador
- Fonte 12V
- Banco de dados MariaDB
- Servidor MQTT (Mosquitto)
- Ambiente Python com Streamlit

### Configuração

1. Monte o circuito conforme o diagrama elétrico (Figura 2 do artigo).
2. Instale o Mosquitto Broker no Raspberry Pi.
3. Configure o ESP32 para publicar leituras do DHT11 via MQTT.
4. Desenvolva um script Python para receber e armazenar os dados no MariaDB.
5. Crie um *dashboard* com Streamlit para visualização.
6. Use o Ngrok para expor o *dashboard* local à internet.

---

## ✅ Conclusões

- Sistema eficaz no controle de umidade e temperatura para conservação de PLA.
- Solução de baixo custo e energeticamente eficiente.
- Ideal para makers, laboratórios e pequenas indústrias de impressão 3D.

---

## 📁 Estrutura do Repositório (Sugerida)

```
/
├── hardware/          # Esquemas elétricos e lista de componentes
├── firmware/          # Código do ESP32 (Arduino/C++)
├── backend/           # Script Python (Raspberry Pi + MQTT + MariaDB)
├── dashboard/         # Código do Streamlit
├── docs/              # Artigo e imagens do projeto
└── README.md
```

---

## 👨‍💻 Autores

- **Thiago de Sena** – [thiago.sena.lima07@aluno.ifce.edu.br](mailto:thiago.sena.lima07@aluno.ifce.edu.br)
- **Fábio Timbó Brito** – [fabio@ifce.edu.br](mailto:fabio@ifce.edu.br)

Instituto Federal de Educação, Ciência e Tecnologia do Ceará – Campus Maracanaú

---

## 📄 Referências

Artigo Completo:
[Construção de uma estufa in situ para conservação de filamentos de PLA para impressão 3D com monitoramento IoT](https://sol.sbc.org.br/busca/index.php/integrada/results?isAdvanced=1&query=&field-3=Constru%C3%A7%C3%A3o+de+estufa+in+situ&field-15=&field-4=&field-14=&field-16=&field-7-fromMonth=&field-7-fromDay=&field-7-fromYear=&field-7-toMonth=&field-7-toDay=&field-7-toYear=) - Disponível no portal da Sociedade Brasileira de Computação (SBC)

Para citações e referências completas, consulte a seção "Referências" do artigo original.

---

> 🔗 *Projeto desenvolvido com apoio do Laboratório Espaço Maker IFCE Maracanaú e DEPPI.*
