#!/bin/bash
source /etc/profile
module load miniconda3/4.5.11_gcc-6.4.0
source activate rllibd

port=16380
redis_address=lille
redis_address="$redis_address:$port"

#./setup_node.sh $redis_address
ray start --address=$redis_address
jupyter lab --no-browser --port 8768 --ip=0.0.0.0 --notebook-dir=/home/emorsi/jupyter
