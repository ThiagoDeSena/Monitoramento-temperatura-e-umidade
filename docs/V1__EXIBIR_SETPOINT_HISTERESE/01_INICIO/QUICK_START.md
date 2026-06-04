## ⚡ QUICK START - Começar em 5 Minutos

### 🚀 Passo 1: Criar a Tabela (NO RASPBERRY PI)

```bash
cd /caminho/do/projeto
mysql -u user01 -p monitoramento < criar_tabela_configuracoes.sql
# Digite senha: pi

# Verificar:
mysql -u user01 -p monitoramento -e "SELECT * FROM configuracoes;"
```

### 🚀 Passo 2: Reiniciar o Serviço MQTT (NO RASPBERRY PI)

```bash
# Se estiver rodando, parar:
systemctl stop mqtt_service

# Iniciar novamente (ele vai carregar o código modificado):
systemctl start mqtt_service

# Verificar:
systemctl status mqtt_service
```

### 🚀 Passo 3: Abrir o Dashboard

```bash
# Na máquina com Streamlit:
streamlit run main.py
# Abre em http://localhost:8501
```

### 🚀 Passo 4: Testar (Publicar MQTT)

```bash
# Em outro terminal no Raspberry Pi:
mosquitto_pub -h localhost -t "monitoramento/setpoint" -m "35.0"
mosquitto_pub -h localhost -t "monitoramento/histerese" -m "2.0"

# No Dashboard, atualize (F5)
# ✅ Você deve ver:
#    🎯 Setpoint: 35.0°C
#    📊 Histerese: 2.0°C
```

---

## 📁 Arquivos Modificados:

| Arquivo | Modificação |
|---------|-------------|
| `mqttClient.py` | ✅ Adicionados tópicos setpoint/histerese |
| `dataProcessor.py` | ✅ Processa e salva setpoint/histerese |
| `databases.py` | ✅ Novos métodos para setpoint/histerese |
| `graphGenerator.py` | ✅ Exibe valores no dashboard |
| `criar_tabela_configuracoes.sql` | ✨ NOVO - Cria tabela no banco |

---

## 🎯 O Que Mudar no Código (Se Necessário):

### Se o MariaDB estiver em outro host:
```python
# Em mqtt_service.py:
db = Database(host="IP_DO_RASPBERRY", user="user01", password="pi", database="monitoramento")
```

### Se a porta MQTT for diferente:
```python
# Em mqtt_service.py:
mqtt_client = MqttClient("localhost", port=1883)  # Mudar a porta aqui
```

---

## 📊 Resultado No Dashboard:

```
📊 Última Leitura        ⚙️ Configurações Atuais
┌──────────┬──────┐     ┌──────────┬──────────┬──────┐
│ 🌡️ 28.5 │ 💧65 │     │ 🎯 35.0  │ 📊 2.0   │ ⏰... │
└──────────┴──────┘     └──────────┴──────────┴──────┘
```

---

## ✅ Verificação Rápida:

```bash
# 1. Tabela existe?
mysql -u user01 -p monitoramento -e "DESC configuracoes;"

# 2. MQTT rodando?
systemctl status mqtt_service

# 3. Dados sendo salvos?
mysql -u user01 -p monitoramento -e "SELECT * FROM configuracoes;"

# 4. Dashboard mostrando?
# Abra http://localhost:8501 e veja seção "⚙️ Configurações Atuais"
```

---

## 🐛 Se Não Funcionar:

1. **"Table not found"** → Execute o Passo 1 novamente
2. **"Sem dados no dashboard"** → Publique MQTT: `mosquitto_pub -h localhost -t "monitoramento/setpoint" -m "35.0"`
3. **"Valores aparecem como --"** → Refreshe o Streamlit (F5 ou clique "Atualizar Gráfico")

---

## 📚 Próximas Leituras:

- [../02_INSTALACAO/GUIA_SETPOINT_HISTERESE.md](../02_INSTALACAO/GUIA_SETPOINT_HISTERESE.md) - Documentação completa
- [../03_IMPLEMENTACAO/RESUMO_IMPLEMENTACAO.md](../03_IMPLEMENTACAO/RESUMO_IMPLEMENTACAO.md) - Como funciona internamente
- [../05_TESTES/TESTE_E_VALIDACAO.md](../05_TESTES/TESTE_E_VALIDACAO.md) - Testes detalhados

---

**Pronto! Você tem um sistema de monitoramento em tempo real! 🚀**
