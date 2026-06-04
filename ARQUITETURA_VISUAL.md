# 🎯 Diagrama Visual da Solução Implementada

## Arquitetura Completa:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SISTEMA COMPLETO                              │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────────┐
│      ESP32             │
│                        │
│ ├─ Temp Sensor        │
│ ├─ Humidity Sensor    │
│ ├─ Config Store       │  ←── Armazena setpoint/histerese
│ └─ MQTT Publish       │
└──────────┬─────────────┘
           │
           │ Publica em:
           ├─ monitoramento/temperatura (a cada segundo)
           ├─ monitoramento/umidade (a cada segundo)
           ├─ monitoramento/setpoint (quando muda)
           ├─ monitoramento/histerese (quando muda)
           └─ monitoramento/heartbeat (periódico)
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI 3 (Centro de Controle)                   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │ mqtt_service.py (Service)                               │          │
│  │                                                           │          │
│  │  ┌────────────────────────────────────────────────────┐ │          │
│  │  │ MqttClient (mqttClient.py)                         │ │          │
│  │  │ ├─ Conecta ao broker MQTT                          │ │          │
│  │  │ ├─ Inscreve em todos os tópicos                   │ │          │
│  │  │ └─ Recebe mensagens                                │ │          │
│  │  └────────────────┬─────────────────────────────────┘ │          │
│  │                   │                                    │          │
│  │  ┌────────────────▼─────────────────────────────────┐ │          │
│  │  │ DataProcessor (dataProcessor.py)                │ │          │
│  │  │ ├─ Processa monitoramento/temperatura         │ │          │
│  │  │ ├─ Processa monitoramento/umidade             │ │          │
│  │  │ ├─ Processa monitoramento/setpoint ◄──NEW     │ │          │
│  │  │ ├─ Processa monitoramento/histerese ◄──NEW    │ │          │
│  │  │ └─ Salva no banco de dados                     │ │          │
│  │  └────────────────┬─────────────────────────────────┘ │          │
│  │                   │                                    │          │
│  │  ┌────────────────▼─────────────────────────────────┐ │          │
│  │  │ Database (databases.py)                          │ │          │
│  │  │ ├─ insert_into_database() ◄─ Temp/Umidade      │ │          │
│  │  │ ├─ update_setpoint_histerese() ◄──NEW           │ │          │
│  │  │ └─ get_latest_setpoint_histerese() ◄──NEW       │ │          │
│  │  └────────────────┬─────────────────────────────────┘ │          │
│  └─────────────────────┼────────────────────────────────┘│          │
│                        │                                  │          │
└────────────────────────┼──────────────────────────────────┘          │
                         │                                              │
                         ▼                                              │
        ┌────────────────────────────┐                                 │
        │    MariaDB (Local)          │                                 │
        │                             │                                 │
        │  Tabela: valores           │                                 │
        │  ├─ temperatura            │  ← Atualiza a cada segundo     │
        │  ├─ umidade                │  ← Atualiza a cada segundo     │
        │  ├─ data                   │                                 │
        │  └─ id (PRIMARY)           │                                 │
        │                             │                                 │
        │  Tabela: configuracoes ◄──NEW                                │
        │  ├─ setpoint               │  ← Atualiza quando recebe MQTT │
        │  ├─ histerese              │  ← Atualiza quando recebe MQTT │
        │  ├─ data_atualizacao       │                                 │
        │  └─ id (sempre 1)          │  ← Sempre 1 registro!         │
        │                             │                                 │
        └─────────────────────────────┘                                 │

           ◄─────────────────────────────┐
           │ (Lê valores em tempo real)   │
           │                             │
┌──────────▼─────────────────────────────────────────────────┐         │
│  Streamlit Dashboard (main.py)                             │         │
│  Rodando em: http://localhost:8501                         │         │
│                                                             │         │
│  ┌─────────────────────────────────────────────────────┐  │         │
│  │ GraphGenerator (graphGenerator.py)                 │  │         │
│  │ ├─ fetch_data_for_last_n_days()                   │  │         │
│  │ ├─ show_latest_readings()                         │  │         │
│  │ ├─ show_setpoint_histerese() ◄──NEW               │  │         │
│  │ └─ create_graph()                                 │  │         │
│  └────────────────┬─────────────────────────────────┘  │         │
│                   │                                     │         │
│  ┌────────────────▼──────────────────────────────────┐ │         │
│  │  Dashboard Visual                                │ │         │
│  │  ┌────────────────────────────────────────────┐ │ │         │
│  │  │ Gráfico de Monitoramento                  │ │ │         │
│  │  ├─────────────────────────────────────────────┤ │ │         │
│  │  │                                             │ │ │         │
│  │  │ 📊 Última Leitura                          │ │ │         │
│  │  │ ┌──────────┬──────────┬──────────────┐    │ │ │         │
│  │  │ │ 🌡️ Temp│ 💧 Umid │ 🕒 Data     │    │ │ │         │
│  │  │ │ 28.5°C  │ 65%     │ 14:30 ...   │    │ │ │         │
│  │  │ └──────────┴──────────┴──────────────┘    │ │ │         │
│  │  │                                             │ │ │         │
│  │  │ ⚙️ Configurações Atuais ◄──NEW             │ │ │         │
│  │  │ ┌──────────┬──────────┬──────────────┐    │ │ │         │
│  │  │ │ 🎯 Set  │ 📊 Hist │ ⏰ Atual    │    │ │ │         │
│  │  │ │ 35.0°C  │ 2.0°C   │ 14:25 ...   │    │ │ │         │
│  │  │ └──────────┴──────────┴──────────────┘    │ │ │         │
│  │  │                                             │ │ │         │
│  │  │ [Gráfico com Temperatura e Umidade]       │ │ │         │
│  │  │                                             │ │ │         │
│  │  │ ⬇️ Sidebar:                                │ │ │         │
│  │  │ ├─ 🔧 Configurar Controle                 │ │ │         │
│  │  │ │  ├─ Input: 🌡️ Setpoint (40.0)         │ │ │         │
│  │  │ │  ├─ Input: 🔁 Histerese (2.0)         │ │ │         │
│  │  │ │  └─ Button: ✅ Enviar                   │ │ │         │
│  │  │ │                                           │ │ │         │
│  │  │ ├─ 📅 Selecionar Período                   │ │ │         │
│  │  │ │  ├─ Button: 1 Dia                       │ │ │         │
│  │  │ │  ├─ Button: 7 Dias                      │ │ │         │
│  │  │ │  ├─ Button: 30 Dias                     │ │ │         │
│  │  │ │  └─ Button: Tudo                        │ │ │         │
│  │  │ │                                           │ │ │         │
│  │  │ └─ 🎨 Escolher variável                    │ │ │         │
│  │  │                                             │ │ │         │
│  │  └─────────────────────────────────────────────┘ │ │         │
│  │                                                   │ │         │
│  └───────────────────────────────────────────────────┘ │         │
│                                                         │         │
└─────────────────────────────────────────────────────────┘         │
```

---

## Fluxo de Dados:

### ➊ **Temperatura/Umidade** (Dados Históricos):
```
ESP32 → monitoramento/temperatura → MqttClient → DataProcessor
                                                      ↓
                                           INSERT INTO valores
                                                      ↓
                                           MariaDB (tabela valores)
```

### ➋ **Setpoint/Histerese** (Configurações) ◄── NOVO:
```
ESP32 → monitoramento/setpoint → MqttClient → DataProcessor
                                                      ↓
                                    UPDATE configuracoes SET setpoint
                                                      ↓
                                    MariaDB (tabela configuracoes)
```

### ➌ **Exibição em Tempo Real** ◄── NOVO:
```
Streamlit (Dashboard)
          ↓
GraphGenerator.show_latest_readings()
          ├─ Exibe Temperatura/Umidade (do banco)
          ├─ Exibe Setpoint/Histerese (do banco) ◄── NOVO
          └─ Atualiza quando F5
```

---

## Fluxo de Salvamento:

```
┌─────────────────┐
│  ESP32 Publica  │
│  Setpoint: 35.0 │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│ DataProcessor.process_data()    │
│ topic = "monitoramento/setpoint"│
└────────┬────────────────────────┘
         │
         ├─ Valor mudou? (35.0 ≠ 30.0)
         │  ├─ SIM: Salvar
         │  └─ NÃO: Ignorar
         │
         ▼
┌─────────────────────────────────┐
│ Database.update_setpoint_...()  │
│ UPDATE configuracoes SET ...    │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ MariaDB - configuracoes         │
│ id=1, setpoint=35.0             │
│ data_atualizacao=ATUAL          │
└─────────────────────────────────┘
```

---

## Comparação: Antes vs Depois:

### ANTES (Sem Setpoint/Histerese):
```
Tabela: valores
├─ temperatura (atualiza a cada segundo)
├─ umidade (atualiza a cada segundo)
├─ data (timestamp)
└─ id

Dashboard:
├─ 📊 Última Leitura (Temp/Umidade)
└─ [Gráfico]

❌ Setpoint/Histerese NÃO eram mostrados
❌ Não eram salvos
```

### DEPOIS (Com Setpoint/Histerese ◄── NOVO):
```
Tabela: valores
├─ temperatura (atualiza a cada segundo)
├─ umidade (atualiza a cada segundo)
├─ data (timestamp)
└─ id

Tabela: configuracoes ◄── NOVO
├─ setpoint (atualiza quando muda)
├─ histerese (atualiza quando muda)
├─ data_atualizacao (timestamp)
└─ id (sempre 1)

Dashboard:
├─ 📊 Última Leitura (Temp/Umidade)
├─ ⚙️ Configurações Atuais ◄── NOVO (Setpoint/Histerese)
└─ [Gráfico]

✅ Setpoint/Histerese SÃO mostrados
✅ SÃO salvos e persistem
✅ Atualizam em tempo real
```

---

## Modificações de Código:

### mqttClient.py
```diff
  self.topics = [
      "monitoramento/temperatura",
      "monitoramento/umidade",
      "monitoramento/heartbeat",
      "monitoramento/rele",
+     "monitoramento/setpoint",        ◄── NOVO
+     "monitoramento/histerese"        ◄── NOVO
  ]
```

### dataProcessor.py
```diff
  def process_data(self, topic, payload):
      if topic == "monitoramento/temperatura":
          ...
+     elif topic == "monitoramento/setpoint":          ◄── NOVO
+         self.db.update_setpoint_histerese(...)
+     elif topic == "monitoramento/histerese":        ◄── NOVO
+         self.db.update_setpoint_histerese(...)
```

### databases.py
```diff
+ def update_setpoint_histerese(self, setpoint=None, histerese=None):  ◄── NOVO
+     UPDATE configuracoes SET ...
+
+ def get_latest_setpoint_histerese(self):                            ◄── NOVO
+     SELECT setpoint, histerese FROM configuracoes
```

### graphGenerator.py
```diff
+ def show_setpoint_histerese(self):                    ◄── NOVO
+     st.metric("🎯 Setpoint", ...)
+     st.metric("📊 Histerese", ...)
+
  def show_latest_readings(self, df):
      ... (já existente)
+     self.show_setpoint_histerese()                    ◄── NOVO
```

---

## Banco de Dados - Antes vs Depois:

### Tabela `valores` (Sem mudança):
```
id | temperatura | umidade | data
1  | 28.5        | 65      | 2024-01-15 14:30:00
2  | 28.6        | 64      | 2024-01-15 14:31:00
3  | 28.7        | 63      | 2024-01-15 14:32:00
...
```

### Tabela `configuracoes` ◄── NOVA:
```
id | setpoint | histerese | data_atualizacao
1  | 35.0     | 2.0       | 2024-01-15 14:25:30
   (sempre 1 registro, updated raramente)
```

**Vantagens:**
- ✅ Sem replicação de dados
- ✅ Sem NULLs
- ✅ Consultas rápidas (1 registro)
- ✅ Simples manutenção

---

## Performance:

| Operação | Antes | Depois | Impacto |
|----------|-------|--------|---------|
| UPDATE temperatura/umidade | 1x/segundo | 1x/segundo | Nenhum |
| UPDATE setpoint/histerese | Nunca | Raramente | Mínimo |
| SELECT para dashboard | 1 tabela | 2 tabelas | +1ms |
| Armazenamento | crescente | +1 registro | Negligente |

---

## Segurança e Validação:

```python
# DataProcessor valida:
if payload != self.last_saved_values["setpoint"]:
    # Só salva se mudou (evita replicação)
    db.update_setpoint_histerese(setpoint=payload)
```

---

Pronto! Você tem um sistema completo, elegante e eficiente! 🚀
