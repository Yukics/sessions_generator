#!/bin/bash
nodeps=$1

if ! [[ -d ".venv"  ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
export PYTHONWARNINGS="ignore" # setuptools >81 warn

echo "[INFO] to skip deps installation use: ./start.sh nodeps"
if [ "$nodeps" != "nodeps" ]; then
    pip -r requirements.txt > /dev/null
fi

cd src
python3 main.py --log=debug
