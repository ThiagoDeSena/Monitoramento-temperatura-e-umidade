## 🚀 Guia: Implementação de Setpoint e Histerese em Tempo Real

### 📋 O que foi feito:

1. **Nova tabela `configuracoes`** - Armazena apenas o **último valor** de setpoint e histerese
2. **Subscrição MQTT** - O cliente agora se inscreve em `monitoramento/setpoint` e `monitoramento/histerese`
3. **Processamento de dados** - O DataProcessor salva esses valores automaticamente no banco
4. **Exibição em tempo real** - O gráfico mostra os valores atualizados imediatamente
5. **Persistência** - Os valores são salvos, então sobrevivem a quedas da aplicação

---

### 📊 Visão Geral da Solução:

```
ESP32 (publica valores)
   ↓
monitoramento/setpoint ──→ MqttClient ──→ DataProcessor ──→ Database (configuracoes)
monitoramento/histerese ──┘                                         ↓
                                                        GraphGenerator (exibe)
```

**Por que tabela separada?**
- ✅ Setpoint/Histerese mudam raramente (não replica a cada segundo)
- ✅ Evita NULLs e desperdício de espaço
- ✅ Consultas rápidas (sempre 1 registro)
- ✅ Fácil de visualizar e manter

---

### ⚙️ Passos de Instalação (NO RASPBERRY PI 3):

#### 1️⃣ Criar a tabela no MariaDB:

```bash
# Via terminal do Raspberry Pi:
cd c:\Users\Rosy\Documents\Maker\Monitoramento-temperatura-e-umidade

# Copie o arquivo para o Raspberry Pi (se necessário)
# Ou execute direto:

mysql -u user01 -p monitoramento
# Digite a senha: pi

# Depois execute:
CREATE TABLE IF NOT EXISTS configuracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setpoint FLOAT NULL DEFAULT NULL,
    histerese FLOAT NULL DEFAULT NULL,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO configuracoes (id, setpoint, histerese) VALUES (1, NULL, NULL);
CREATE INDEX idx_data ON configuracoes(data_atualizacao);

# Exit
exit;
```

**OU use o arquivo SQL preparado:**
```bash
mysql -u user01 -p monitoramento < criar_tabela_configuracoes.sql
```

#### 2️⃣ Verificar que a tabela foi criada:

```bash
mysql -u user01 -p monitoramento -e "SELECT * FROM configuracoes;"
# Esperado:
# | id | setpoint | histerese | data_atualizacao |
# |  1 | NULL     | NULL      | 2024-XX-XX ...   |
```

---

### 🔄 Fluxo de Funcionamento:

#### **Quando o ESP32 publica setpoint:**
```
monitoramento/setpoint → 35.5
                           ↓
                    DataProcessor
                           ↓
        UPDATE configuracoes SET setpoint=35.5
                           ↓
        Database salva (imediatamente)
```

#### **Quando você abrir o Streamlit:**
```
GraphGenerator.show_latest_readings()
         ↓
  show_setpoint_histerese()
         ↓
  get_latest_setpoint_histerese()
         ↓
  Exibe com st.metric (em tempo real)
```

---

### 🖼️ Como o Dashboard ficará:

```
┌─────────────────────────────────────────────────┐
│       Gráfico de Monitoramento                  │
├─────────────────────────────────────────────────┤
│                                                 │
│    📊 Última Leitura                           │
│  ┌──────────┬──────────┬──────────────────┐   │
│  │ 🌡️ T    │ 💧 U     │ 🕒 Data/Hora    │   │
│  │ 28.5°C   │ 65%      │ 2024-01-15 14:30│   │
│  └──────────┴──────────┴──────────────────┘   │
│                                                 │
│    ⚙️ Configurações Atuais                     │
│  ┌──────────┬──────────┬──────────────────┐   │
│  │ 🎯 Set   │ 📊 Hist  │ ⏰ Atualizado   │   │
│  │ 35.0°C   │ 2.0°C    │ 2024-01-15 14:20│   │
│  └──────────┴──────────┴──────────────────┘   │
│                                                 │
│       [Gráfico com Temperatura e Umidade]     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

### 🔍 Dados Armazenados no Banco:

**Tabela `valores` (já existente):**
```
id | temperatura | umidade | data
1  | 28.5        | 65      | 2024-01-15 14:30:00
2  | 28.6        | 64      | 2024-01-15 14:31:00
...
```

**Tabela `configuracoes` (nova):**
```
id | setpoint | histerese | data_atualizacao
1  | 35.0     | 2.0       | 2024-01-15 14:20:00
```

---

### 📝 Exemplos de Uso:

#### **1. O ESP32 publica setpoint:**
```
MQTT Pub → monitoramento/setpoint : 40.5
DataProcessor recebe → Salva automaticamente no banco
Streamlit mostra → 🎯 Setpoint: 40.5°C
```

#### **2. Aplicação cai e volta:**
```
Streamlit inicia
GraphGenerator.show_setpoint_histerese()
Consulta banco → Recupera 40.5 (persistido)
Exibe o valor correto ✓
```

#### **3. Atualizando via dashboard:**
```
Usuário entra: Setpoint = 38.0
Clica: ✅ Enviar Setpoint/Histerese
MQTT Pub → monitoramento/setpoint : 38.0
DataProcessor recebe → Salva
Streamlit atualiza → 🎯 Setpoint: 38.0°C
```

---

### ✅ Checklist de Verificação:

- [ ] Tabela `configuracoes` foi criada no MariaDB
- [ ] `mqttClient.py` tem os tópicos `monitoramento/setpoint` e `monitoramento/histerese`
- [ ] `dataProcessor.py` processa esses tópicos e salva no banco
- [ ] `databases.py` tem os métodos `update_setpoint_histerese()` e `get_latest_setpoint_histerese()`
- [ ] `graphGenerator.py` tem o método `show_setpoint_histerese()` e mostra no dashboard
- [ ] O serviço MQTT (`mqtt_service.py`) está rodando no Raspberry Pi
- [ ] O Streamlit (`main.py`) mostra os valores atualizados

---

### 🐛 Troubleshooting:

**Problema: "Erro ao atualizar setpoint"**
- Verifique se a tabela `configuracoes` existe: `SHOW TABLES;`
- Verifique se tem um registro com id=1: `SELECT * FROM configuracoes;`

**Problema: Valores aparecem como "--"**
- Verifique se o ESP32 está publicando: `mosquitto_sub -h localhost -t "monitoramento/#"`
- Verifique os logs do `mqtt_service.py` no Raspberry Pi

**Problema: Valores não persistem**
- Verifique se a conexão ao MariaDB está funcionando
- Verifique os logs: `journalctl -u mqtt_service -f`

---

### 📚 Arquivos Modificados:

1. `mqttClient.py` - Adicionou tópicos de setpoint/histerese
2. `dataProcessor.py` - Adicionou processamento de setpoint/histerese
3. `databases.py` - Adicionou métodos de atualização e leitura
4. `graphGenerator.py` - Adicionou exibição visual
5. `criar_tabela_configuracoes.sql` - Script para criar a tabela

---

### 🚀 Próximos Passos (Opcional):

- [ ] Adicionar gráfico histórico de mudanças de setpoint/histerese
- [ ] Implementar alertas quando setpoint/histerese mudam
- [ ] Exportar configurações para CSV
- [ ] Adicionar validações de limites (min/max)
