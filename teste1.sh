#!/bin/bash

AMBIENTE_VIRTUAL="/home/pi/ProgramasRasp/teste/venv1"
SCRIPT_PYTHON="/home/pi/ProgramasRasp/teste/main.py"

source $AMBIENTE_VIRTUAL/bin/activate
streamlit run $SCRIPT_PYTHON
