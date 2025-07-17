#!/bin/bash

# Ambiente Virtual
AMBIENTE_VIRTUAL="/home/pi/ProgramasRasp/teste/venv1"

# CAminho dos Scripts
SCRIPT_PYTHON="/home/pi/ProgramasRasp/teste/main.py"
SCRIPT_MQTT="/home/pi/ProgramasRasp/teste/mqtt_service.py"

# Ativa Ambiente Virtual
source $AMBIENTE_VIRTUAL/bin/activate

# Inicia o serviço MQTT em background com redirecionamento de logs
python3 $SCRIPT_MQTT >> /home/pi/ProgramasRasp/teste/log_mqtt.log 2>&1 &

# Inicia a aplicação Streamlit (isso fica em foreground para o .service monitorar)
streamlit run $SCRIPT_PYTHON
