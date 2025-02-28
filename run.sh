#!/bin/bash

usage() {
    echo "Uso: $0 --dias <N_DIAS>"
    exit 1
}

if [ "$1" != "--dias" ] || [ -z "$2" ]; then
    usage
fi

DAYS="$2"
if ! dpkg -s python3.10-venv >/dev/null 2>&1; then
    sudo apt update
    sudo apt install python3.10-venv
fi


if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py $DAYS