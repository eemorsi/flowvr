#!/bin/bash
source /etc/profile
module load miniconda3/4.5.11_gcc-6.4.0
source activate rllibd
jupyter lab --no-browser --port 8768 --ip=0.0.0.0 --notebook-dir=/home/emorsi/jupyter
