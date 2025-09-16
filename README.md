# Solução para "Illegal Instruction" no Raspberry Pi

## Problema
Após fazer upgrade do Raspberry Pi OS, aplicações Streamlit começaram a apresentar o erro `illegal instruction` ao tentar importar bibliotecas como pandas, numpy, yfinance, etc.

## Causa
O erro ocorre devido à incompatibilidade entre bibliotecas compiladas (principalmente PyArrow) e a nova arquitetura/versão do Python após o upgrade do sistema.

## Solução Completa

### 1. Instalar Dependências do Sistema
```bash
sudo apt update
sudo apt install python3-pandas python3-numpy python3-scipy
```

### 2. Criar Ambiente Virtual com Acesso às Bibliotecas do Sistema
```bash
# Remover ambiente virtual antigo
rm -rf venv

# Criar novo ambiente com acesso às bibliotecas do sistema
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

### 3. Instalar Streamlit sem Dependências
```bash
pip install --no-deps streamlit
```

### 4. Instalar Dependências Básicas do Streamlit
```bash
pip install protobuf cachetools tornado watchdog toml tzlocal validators jsonschema rich typer packaging urllib3 requests
```

### 5. Instalar Bibliotecas Problemáticas com Versões Específicas
```bash
# Instalar bibliotecas uma por vez para identificar problemas
pip install altair
pip install gitpython

# IMPORTANTE: Use versão específica do PyArrow que funciona no ARM
pip install pyarrow==12.0.0

pip install pydeck
pip install tenacity
```

### 6. Instalar Suas Bibliotecas Específicas
```bash
pip install paho-mqtt mariadb
pip install --no-deps yfinance beautifulsoup4 multitasking platformdirs pytz frozendict peewee websockets
```

## Biblioteca Culpada
O **PyArrow** é a principal causa do problema. A versão mais recente não é compatível com o processador ARM do Raspberry Pi. Use sempre a versão `12.0.0`:

```bash
pip install pyarrow==12.0.0
```

## Correções de Código Necessárias

### Plotly (se usar)
Versões mais novas do Plotly mudaram a sintaxe:

**❌ Sintaxe antiga:**
```python
yaxis=dict(
    title="Título",
    titlefont=dict(color="red")  # ERRO
)
```

**✅ Sintaxe nova:**
```python
yaxis=dict(
    title="Título", 
    title_font=dict(color="red")  # CORRETO
)
```

## Teste Final
```bash
# Teste básico
streamlit hello

# Teste sua aplicação
streamlit run main.py
```

## Informações do Sistema Testado
- **Raspberry Pi OS:** Bullseye (Debian 11)
- **Python:** 3.11.2
- **Arquitetura:** ARM
- **PyArrow:** 12.0.0 (versão que funciona)

## Dica Importante
Sempre use `--system-site-packages` ao criar o venv para ter acesso às bibliotecas já compiladas do sistema, evitando problemas de compilação no ARM.

## Resolução de Problemas

### Se ainda der "illegal instruction":
1. Verifique qual biblioteca específica está causando o erro
2. Tente versões mais antigas da biblioteca problemática
3. Use as versões do sistema quando disponível: `sudo apt install python3-[biblioteca]`

### Se pip der conflitos de dependência:
```bash
pip install --force-reinstall [biblioteca]==versão_específica
```

### Para identificar biblioteca problemática:
Importe uma por vez no Python interativo até encontrar a que causa o erro:
```python
python3
import pandas     # teste
import numpy      # teste  
import pyarrow    # teste
import yfinance   # teste
```
