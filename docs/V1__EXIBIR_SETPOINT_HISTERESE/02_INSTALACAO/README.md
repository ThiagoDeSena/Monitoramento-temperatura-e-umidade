# ⚙️ 02 - INSTALAÇÃO

## Passo a Passo da Instalação

Esta pasta contém **tudo que você precisa para instalar o sistema**.

### 📄 Arquivos:

1. **GUIA_SETPOINT_HISTERESE.md** (Documentação Completa)
   - Visão geral da solução
   - Passos detalhados de instalação
   - Fluxo de funcionamento
   - Exemplos de uso
   - Troubleshooting avançado

2. **INSTALL.sh** (Script Bash)
   - Checklist executável
   - Comandos prontos para copiar/colar
   - Instruções passo a passo

3. **criar_tabela_configuracoes.sql** (SQL)
   - Script SQL pronto
   - Cria tabela `configuracoes`
   - Pronto para executar no MariaDB

---

## 🎯 Passo a Passo Rápido:

### 1️⃣ Criar Tabela (NO RASPBERRY PI):
```bash
mysql -u user01 -p monitoramento < criar_tabela_configuracoes.sql
# Digite senha: pi
```

### 2️⃣ Reiniciar Serviço (NO RASPBERRY PI):
```bash
systemctl restart mqtt_service
```

### 3️⃣ Abrir Dashboard (NA SUA MÁQUINA):
```bash
streamlit run main.py
```

### 4️⃣ Testar (NO RASPBERRY PI):
```bash
mosquitto_pub -h localhost -t "monitoramento/setpoint" -m "35.0"
mosquitto_pub -h localhost -t "monitoramento/histerese" -m "2.0"
```

---

## 📚 Para Mais Detalhes:

- **Instalação Completa** → `GUIA_SETPOINT_HISTERESE.md`
- **Script com Checklist** → `INSTALL.sh`
- **SQL pronto** → `criar_tabela_configuracoes.sql`

---

## 🔗 Outras Pastas:

- ⬅️ [01_INICIO](../01_INICIO/README.md) - Quick Start
- ➡️ [03_IMPLEMENTACAO](../03_IMPLEMENTACAO/README.md) - O que mudou
- ➡️ [04_ARQUITETURA](../04_ARQUITETURA/README.md) - Diagramas
- ➡️ [05_TESTES](../05_TESTES/README.md) - Validação

---

**Próximo: Leia GUIA_SETPOINT_HISTERESE.md** 📖
