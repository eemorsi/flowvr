#!/bin/bash
source /etc/profile
# module load miniconda3/4.5.11_gcc-6.4.0
# source activate rllibd
export PATH=$PATH:/home/emorsi/.local/bin

ray start --address=$1


source $2/bin/flowvr-suite-config.sh 
flowvrd > /dev/null 2>&1 &


