# 📊 Resumo da Implementação: Setpoint e Histerese em Tempo Real

## ✅ O que foi implementado:

### 1. **Banco de Dados** 🗄️
- ✅ Nova tabela `configuracoes` para armazenar apenas o último valor de setpoint e histerese
- ✅ Sem NULLs ou replicação desnecessária

### 2. **MQTT Client** 📡
- ✅ Subscrição nos tópicos:
  - `monitoramento/setpoint`
  - `monitoramento/histerese`

### 3. **Data Processor** ⚙️
- ✅ Processa mensagens de setpoint/histerese
- ✅ Salva automaticamente no banco ao receber

### 4. **Database Methods** 💾
- ✅ `update_setpoint_histerese()` - Atualiza valores
- ✅ `get_latest_setpoint_histerese()` - Recupera valores

### 5. **Visualização** 📈
- ✅ Novo método `show_setpoint_histerese()` 
- ✅ Exibe valores com st.metric (visual limpo)
- ✅ Mostra data da última atualização
- ✅ Integrado no dashboard principal

---

## 🎯 Fluxo Completo:

```
┌─────────────────────────────────────────────────────────┐
│ ESP32 publica nos tópicos MQTT                         │
└──────┬──────────────────────────────────────────────────┘
       │
       ├─→ monitoramento/setpoint: "40.5"
       └─→ monitoramento/histerese: "2.0"
       
       ↓
┌──────────────────────────────────────────────────────────┐
│ MqttClient recebe as mensagens                          │
│ (mqtt_service.py rodando no Raspberry Pi)              │
└──────┬───────────────────────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────────────────────┐
│ DataProcessor.process_data()                            │
│ └─→ Detecta que é setpoint/histerese                    │
│ └─→ Chama db.update_setpoint_histerese()               │
└──────┬───────────────────────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────────────────────┐
│ Database.update_setpoint_histerese()                    │
│ └─→ UPDATE configuracoes SET setpoint=40.5             │
└──────┬───────────────────────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────────────────────┐
│ Dado salvo no MariaDB                                   │
│ (MariaDB no Raspberry Pi)                              │
└──────┬───────────────────────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────────────────────┐
│ Streamlit Dashboard (main.py)                           │
│ GraphGenerator.show_setpoint_histerese()                │
│ └─→ Recupera: db.get_latest_setpoint_histerese()       │
│ └─→ Exibe: 🎯 Setpoint 40.5°C | 📊 Histerese 2.0°C   │
└──────────────────────────────────────────────────────────┘
```

---

## 💾 Estrutura do Banco de Dados:

### Tabela `valores` (temperatura e umidade - dados históricos):
```sql
id | temperatura | umidade | data
1  | 28.5        | 65      | 2024-01-15 14:30:00
2  | 28.6        | 64      | 2024-01-15 14:31:00
3  | 28.7        | 63      | 2024-01-15 14:32:00
... (muitos registros, atualizado a cada segundo)
```

### Tabela `configuracoes` (setpoint e histerese - apenas último valor):
```sql
id | setpoint | histerese | data_atualizacao
1  | 40.5     | 2.0       | 2024-01-15 14:25:30
   (sempre 1 registro, atualizado raramente)
```

---

## 🛠️ Arquivos Modificados:

### 📝 [mqttClient.py](mqttClient.py)
```diff
  self.topics = [
      "monitoramento/temperatura",
      "monitoramento/umidade",
      "monitoramento/heartbeat",
      "monitoramento/rele",
+     "monitoramento/setpoint",
+     "monitoramento/histerese"
  ]
```

### 📝 [dataProcessor.py](dataProcessor.py)
```diff
  # Adicionados ao __init__:
+     "setpoint": None,
+     "histerese": None
  
  # Novo processamento:
+     elif topic == "monitoramento/setpoint":
+         self.db.update_setpoint_histerese(setpoint=payload)
+     elif topic == "monitoramento/histerese":
+         self.db.update_setpoint_histerese(histerese=payload)
```

### 📝 [databases.py](databases.py)
```python
# Novos métodos:

def update_setpoint_histerese(self, setpoint=None, histerese=None):
    """Atualiza setpoint e/ou histerese na tabela configuracoes"""
    # ... atualiza no banco

def get_latest_setpoint_histerese(self):
    """Recupera o último setpoint e histerese"""
    # ... retorna dicionário com valores
```

### 📝 [graphGenerator.py](graphGenerator.py)
```python
# Novo método:

def show_setpoint_histerese(self):
    """Exibe visualmente setpoint, histerese e data de atualização"""
    # ... usa st.metric para exibição limpa

# Modificado:

def show_latest_readings(self, df):
    # ... já existente
    # + Chama show_setpoint_histerese() ao final
```

### 📝 [criar_tabela_configuracoes.sql](criar_tabela_configuracoes.sql)
```sql
CREATE TABLE IF NOT EXISTS configuracoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setpoint FLOAT NULL,
    histerese FLOAT NULL,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

---

## 🚀 Como Usar:

### 1️⃣ **Criar a tabela (no Raspberry Pi):**
```bash
mysql -u user01 -p monitoramento < criar_tabela_configuracoes.sql
```

### 2️⃣ **Rodar a aplicação MQTT (Raspberry Pi):**
```bash
python mqtt_service.py
```

### 3️⃣ **Abrir o Dashboard (em qualquer máquina na rede):**
```bash
streamlit run main.py
```

### 4️⃣ **Ver os valores atualizados em tempo real:**
- Última Leitura → Temperatura e Umidade (atualizado a cada segundo)
- Configurações Atuais → Setpoint e Histerese (atualizado quando o ESP32 publica)

---

## 🎨 Como ficará na interface:

```
┌─ Gráfico de Monitoramento ──────────────────────────────────┐
│                                                              │
│  📊 Última Leitura                                          │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │ 🌡️ Temp     │ 💧 Umidade  │ 🕒 Data/Hora       │    │
│  │   28.5°C     │    65%      │ 2024-01-15 14:30   │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
│                                                              │
│  ⚙️ Configurações Atuais                                    │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │ 🎯 Setpoint │ 📊 Histerese │ ⏰ Atualizado      │    │
│  │   40.5°C     │    2.0°C     │ 2024-01-15 14:25   │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
│                                                              │
│  [Gráfico com Temperatura e Umidade]                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## ✨ Vantagens da Solução:

✅ **Sem Replicação de Dados** - Setpoint/Histerese mudam raramente
✅ **Sem NULLs** - Tabela separada evita colunas vazias
✅ **Persistência** - Valores sobrevivem a quedas da app
✅ **Tempo Real** - Atualiza automaticamente quando ESP32 publica
✅ **Interface Limpa** - st.metric() exibe de forma elegante
✅ **Fácil Manutenção** - Lógica simples e centralizada

---

## 🔧 Próximas Otimizações (Opcional):

- [ ] Adicionar gráfico histórico de mudanças de setpoint
- [ ] Implementar alertas de mudança
- [ ] Validar limites (min/max) antes de salvar
- [ ] Exportar relatório de configurações
- [ ] Adicionar versionamento de mudanças

---

## 📞 Suporte:

Se alguma coisa não funcionar, verifique:

1. **Tabela existe?** `SELECT * FROM configuracoes;`
2. **MQTT conectado?** `mosquitto_sub -h localhost -t "monitoramento/#"`
3. **Dados sendo salvos?** Verifique os logs do `mqtt_service.py`
4. **Streamlit mostrando?** Verifique se `show_setpoint_histerese()` é chamado

---

Pronto! 🎉 Seu sistema agora está monitorando setpoint e histerese em tempo real!
