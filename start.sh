#!/bin/bash

if ! [[ -d ".venv"  ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
export PYTHONWARNINGS="ignore" # setuptools >81 warn

echo "[INFO] pass withdeps to install dependencies from requirements.txt"
if [ "$1" == "withdeps" ]; then
    pip -r requirements.txt > /dev/null
fi

cd src
python3 main.py --log=debug
