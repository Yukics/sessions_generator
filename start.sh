#!/bin/bash

if ! [[ -d ".venv"  ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
export PYTHONWARNINGS="ignore" # setuptools >81 warn

echo "[INFO] pass "withdeps" as args to install dependencies from requirements.txt"
if [ "$1" == "withdeps" ]; then
    pip3 install -r requirements.txt
fi

cd src
python3 main.py --log=debug
