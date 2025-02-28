#!/bin/bash

usage() {
    echo "Uso: $0 --dias <N_DIAS>"
    exit 1
}

if [ "$1" != "--dias" ] || [ -z "$2" ]; then
    usage
fi

DAYS="$2"

source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py $DAYS