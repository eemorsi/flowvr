#!/bin/bash
source /etc/profile
module load miniconda3/4.5.11_gcc-6.4.0
source activate rllibd
ray stop
