#!/bin/bash
# 📋 CHECKLIST EXECUTÁVEL - Setpoint e Histerese em Tempo Real
# Copie e cole os comandos abaixo no terminal do Raspberry Pi

echo "🚀 Começando implementação de Setpoint e Histerese..."
echo ""

# ✅ PASSO 1: Criar tabela no MariaDB
echo "📝 PASSO 1: Criar tabela no MariaDB..."
echo "Executar no Raspberry Pi:"
echo ""
echo "mysql -u user01 -p monitoramento < criar_tabela_configuracoes.sql"
echo ""
echo "OU manualmente:"
echo "mysql -u user01 -p monitoramento"
echo "CREATE TABLE IF NOT EXISTS configuracoes ("
echo "    id INT AUTO_INCREMENT PRIMARY KEY,"
echo "    setpoint FLOAT NULL DEFAULT NULL,"
echo "    histerese FLOAT NULL DEFAULT NULL,"
echo "    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
echo ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
echo ""
echo "INSERT IGNORE INTO configuracoes (id, setpoint, histerese) VALUES (1, NULL, NULL);"
echo "exit;"
echo ""

# ✅ PASSO 2: Verificar tabela
echo "🔍 PASSO 2: Verificar se tabela foi criada..."
echo "mysql -u user01 -p monitoramento -e 'DESC configuracoes;'"
echo "mysql -u user01 -p monitoramento -e 'SELECT * FROM configuracoes;'"
echo ""

# ✅ PASSO 3: Reiniciar serviço MQTT
echo "🔄 PASSO 3: Reiniciar mqtt_service..."
echo "systemctl restart mqtt_service"
echo ""

# ✅ PASSO 4: Verificar status do serviço
echo "📊 PASSO 4: Verificar se mqtt_service está rodando..."
echo "systemctl status mqtt_service"
echo ""

# ✅ PASSO 5: Abrir Dashboard
echo "🖥️  PASSO 5: Abrir Dashboard Streamlit..."
echo "streamlit run main.py"
echo ""

# ✅ PASSO 6: Testar publicação MQTT
echo "🧪 PASSO 6: Testar publicação MQTT (em outro terminal do Raspberry Pi)..."
echo ""
echo "mosquitto_pub -h localhost -t 'monitoramento/setpoint' -m '35.0'"
echo "mosquitto_pub -h localhost -t 'monitoramento/histerese' -m '2.0'"
echo ""

# ✅ PASSO 7: Verificar no banco
echo "✅ PASSO 7: Verificar se dados foram salvos..."
echo "mysql -u user01 -p monitoramento -e 'SELECT * FROM configuracoes;'"
echo ""

# ✅ PASSO 8: Verificar no dashboard
echo "📈 PASSO 8: Atualizar Dashboard (F5) e verificar seção 'Configurações Atuais'"
echo ""

echo "================================"
echo "✨ SE TODOS OS PASSOS FUNCIONAREM:"
echo "================================"
echo ""
echo "✅ Tabela criada"
echo "✅ Dados salvos no banco"
echo "✅ MQTT funcionando"
echo "✅ Dashboard exibindo setpoint/histerese"
echo "✅ Sistema pronto! 🎉"
echo ""

echo "❌ SE ALGO NÃO FUNCIONAR:"
echo "Leia: TESTE_E_VALIDACAO.md"
echo ""
