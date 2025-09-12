#!/bin/bash

if ! [[ -d ".venv"  ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
export PYTHONWARNINGS="ignore" # setuptools >81 warn

echo "[INFO] pass "withdeps" as args to install dependencies"
if [ "$1" == "withdeps" ]; then
    pip3 install ansible
fi

ansible-playbook -i inventories/inventory.ini playbooks/main.yml