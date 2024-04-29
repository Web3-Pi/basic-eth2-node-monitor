#!/usr/bin/env bash

set -e
cd /opt/web3pi/basic-eth2-node-monitor
source "venv/bin/activate"
python3 -m pip install -r requirements.txt
python3 -u nodemonitor.py -sn "${HOSTNAME}.local" d -db localhost
