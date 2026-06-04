## 🧪 Guia de Teste e Validação

### ✅ Checklist Antes de Iniciar:

- [ ] Tabela `configuracoes` criada no MariaDB
- [ ] Arquivo `criar_tabela_configuracoes.sql` copiado para Raspberry Pi
- [ ] `mqtt_service.py` está rodando no Raspberry Pi
- [ ] `mqttClient.py` contém tópicos de setpoint/histerese
- [ ] `dataProcessor.py` processa esses tópicos
- [ ] `databases.py` tem os novos métodos
- [ ] `graphGenerator.py` chama `show_setpoint_histerese()`
- [ ] Streamlit instalado na máquina

---

## 🧬 Teste 1: Validar a Tabela no MariaDB

### No Raspberry Pi:

```bash
# Conectar ao MariaDB
mysql -u user01 -p monitoramento

# Verificar se a tabela existe
SHOW TABLES;
# Deve mostrar: configuracoes, valores

# Verificar estrutura
DESCRIBE configuracoes;
# Esperado:
# | Field               | Type             | Null | Key | Default |
# | id                  | int(11)          | NO   | PRI | NULL    |
# | setpoint            | float            | YES  |     | NULL    |
# | histerese           | float            | YES  |     | NULL    |
# | data_atualizacao    | timestamp        | NO   |     | CURRENT |

# Verificar dados
SELECT * FROM configuracoes;
# Esperado:
# | id | setpoint | histerese | data_atualizacao        |
# |  1 | NULL     | NULL      | 2024-01-15 14:00:00    |

# Sair
exit;
```

---

## 🧬 Teste 2: Simular Publicação MQTT

### No Raspberry Pi (ou em outro terminal):

```bash
# Terminal 1: Inscrever-se em todos os tópicos
mosquitto_sub -h localhost -t "monitoramento/#" -v

# Terminal 2: Publicar setpoint
mosquitto_pub -h localhost -t "monitoramento/setpoint" -m "35.5"

# Terminal 3: Publicar histerese
mosquitto_pub -h localhost -t "monitoramento/histerese" -m "2.0"

# Esperado no Terminal 1:
# monitoramento/setpoint 35.5
# monitoramento/histerese 2.0
```

---

## 🧬 Teste 3: Verificar Persistência no Banco

### Após publicar MQTT (Teste 2):

```bash
# No Raspberry Pi:
mysql -u user01 -p monitoramento -e "SELECT * FROM configuracoes;"

# Esperado:
# | id | setpoint | histerese | data_atualizacao        |
# |  1 | 35.5     | 2         | 2024-01-15 14:XX:XX    |
```

---

## 🧬 Teste 4: Verificar Logs do mqtt_service.py

```bash
# No Raspberry Pi, verifique os logs:
journalctl -u mqtt_service -f

# Esperado:
# [2024-01-15 14:XX:XX] Setpoint atualizado: 35.5
# [2024-01-15 14:XX:XX] Histerese atualizada: 2.0
```

---

## 🧬 Teste 5: Verificar Visualização no Streamlit

### Na máquina com Streamlit:

```bash
# Abrir a aplicação
streamlit run main.py

# Abrir browser em: http://localhost:8501

# Esperado:
# 1. ✅ Título: "Gráfico de Monitoramento"
# 2. ✅ Seção: "📊 Última Leitura"
#    - 🌡️ Temperatura: XX.X°C
#    - 💧 Umidade: XX%
#    - 🕒 Data/Hora
# 3. ✅ Seção: "⚙️ Configurações Atuais"
#    - 🎯 Setpoint: 35.5°C
#    - 📊 Histerese: 2.0°C
#    - ⏰ Atualizado em: 2024-01-15 14:XX:XX
```

---

## 🧪 Teste 6: Teste de Atualização em Tempo Real

### Passo a Passo:

```
1. Abra o Streamlit (Dashboard)
2. Em outra aba/terminal, publique novo setpoint:
   mosquitto_pub -h localhost -t "monitoramento/setpoint" -m "38.0"
   
3. Volte ao Dashboard
4. Atualizar a página (F5 ou clique em "Atualizar Gráfico")
   
5. ✅ Esperado: 🎯 Setpoint mudou de 35.5 para 38.0
```

---

## 🧪 Teste 7: Teste de Persistência (Queda da App)

### Passo a Passo:

```
1. Abra o Streamlit
2. Veja que Setpoint = 35.5°C
3. Feche o Streamlit (Ctrl+C)
4. Aguarde 5 segundos
5. Abra novamente: streamlit run main.py
6. ✅ Esperado: Setpoint AINDA É 35.5°C (recuperado do banco)
```

---

## 🧪 Teste 8: Teste via Dashboard (Envio de Setpoint)

### Passo a Passo:

```
1. Abra o Dashboard Streamlit
2. Na barra lateral esquerda, procure por:
   "🔧 Configurar Controle"
   
3. Insira valores:
   - 🌡️ Setpoint de Temperatura: 40.0
   - 🔁 Histerese: 2.5
   
4. Clique: "✅ Enviar Setpoint/Histerese"
5. Esperado: "Setpoint (40.0 °C) e Histerese (2.5 °C) enviados com sucesso!"
6. Atualizar Dashboard (F5)
7. ✅ Esperado: Seção "⚙️ Configurações Atuais" mostra os novos valores
```

---

## ⚠️ Possíveis Erros e Soluções:

### Erro: "Erro ao atualizar setpoint: (1146, "Table 'monitoramento.configuracoes' doesn't exist")"

**Solução:**
```bash
mysql -u user01 -p monitoramento < criar_tabela_configuracoes.sql
```

---

### Erro: "Erro ao recuperar configurações: (2006, 'MySQL server has gone away')"

**Solução:**
- Verifique se MariaDB está rodando: `systemctl status mariadb`
- Reinicie: `systemctl restart mariadb`

---

### Erro: Streamlit mostra "🎯 Setpoint: --"

**Possíveis Causas:**
1. Tabela não foi criada
2. Nenhuma mensagem MQTT foi publicada ainda
3. Banco desconectado

**Solução:**
```bash
# Verificar tabela
mysql -u user01 -p monitoramento -e "SELECT * FROM configuracoes;"

# Se vazio, publicar manualmente:
mosquitto_pub -h localhost -t "monitoramento/setpoint" -m "35.0"

# Atualizar Streamlit
```

---

### Erro: "monitoramento/setpoint: command not found"

**Solução:**
- Instalar mosquitto_clients:
```bash
sudo apt-get install mosquitto-clients
```

---

## 📊 Resultado Esperado Final:

### Dashboard no Streamlit:

```
┌─────────────────────────────────────────────────┐
│ Gráfico de Monitoramento                        │
├─────────────────────────────────────────────────┤
│                                                 │
│ 📊 Última Leitura                              │
│ ┌──────────┬──────────┬──────────────────┐    │
│ │ 🌡️ Temp │ 💧 Umid │ 🕒 Data/Hora   │    │
│ │ 28.5°C   │  65%    │ 2024-01-15 ... │    │
│ └──────────┴──────────┴──────────────────┘    │
│                                                 │
│ ⚙️ Configurações Atuais                        │
│ ┌──────────┬──────────┬──────────────────┐    │
│ │ 🎯 Set   │ 📊 Hist │ ⏰ Atualizado  │    │
│ │ 35.5°C   │  2.0°C  │ 2024-01-15 ... │    │
│ └──────────┴──────────┴──────────────────┘    │
│                                                 │
│ [Gráfico com Temp e Umidade]                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## ✨ Validação Completa:

Quando TODOS os testes passarem:

✅ Tabela criada
✅ Dados persistidos no banco
✅ MQTT publica/recebe corretamente
✅ DataProcessor salva valores
✅ Streamlit exibe valores
✅ Atualiza em tempo real
✅ Persiste após queda

**Parabéns! 🎉 Sistema funcionando 100%**

---

## 📝 Notas de Operação:

1. **MQTT Service deve estar rodando:**
   ```bash
   systemctl status mqtt_service
   # ou
   ps aux | grep mqtt_service
   ```

2. **Streamlit reinicia a cada mudança:**
   - É normal aparecer "Rerunning..." 
   - Setpoint/Histerese vêm do banco, então mantêm o valor

3. **Dados históricos:**
   - Tabela `valores` cresce continuamente (temperatura/umidade a cada segundo)
   - Tabela `configuracoes` tem sempre 1 registro (setpoint/histerese atualizam no mesmo registro)

4. **Performance:**
   - Nenhum impacto significativo
   - SELECT em tabela com 1 registro é muito rápido
   - UPDATE também é instantâneo

---

## 🔍 Monitoramento Contínuo:

Para ver tudo funcionando em tempo real em um terminal:

```bash
watch -n 1 'mysql -u user01 -p monitoramento -e "SELECT * FROM configuracoes;"'
```

Isso atualiza a tela a cada 1 segundo mostrando os valores atuais.

---

Pronto! Você tem um sistema completo de monitoramento em tempo real! 🚀
