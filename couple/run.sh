#!bin/bash

export PATH=$PATH:$HOME/.local/bin
source /home/emorsi/pdi/build/bin/flowvr-suite-config.sh

ray start --head --port=16380 --webui-host 0.0.0.0

python3 tictac.py
flowvr -p tictac &
python3 getter.py $1 $2