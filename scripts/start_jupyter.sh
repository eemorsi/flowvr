#!/bin/bash
source /etc/profile
# module load miniconda3/4.5.11_gcc-6.4.0
# source activate rllibd

# Source PDI and FlowVR to allow Jupyter to interact with the python paths correctly 
source /home/emorsi/pdi/build/flowvr/bin/flowvr-suite-config.sh
source /home/emorsi/pdi/build/pdi/share/pdi/env.bash 

export PATH=$PATH:$HOME/.local/bin


jupyter lab --no-browser --port 8768 --ip=0.0.0.0 --notebook-dir=/home/emorsi/jupyter
