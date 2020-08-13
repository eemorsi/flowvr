#!/bin/bash
source /etc/profile
# module load miniconda3/4.5.11_gcc-6.4.0
# source activate rllibd
#----------------------------------------------
# using virtualenv with pdi cause problems with the dist-packages
# instead install ray with pip3 and use it 
# pip3 install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp37-cp37m-manylinux1_x86_64.whl

export PATH=$PATH:$HOME/.local/bin
#----------------------------------------------


port=16380
redis_address="$(hostname --ip-address)"
redis_address="$redis_address:$port"

flowvr_home=$HOME/pdi/build/flowvr
scripts_home=`pwd`

ray start --head --redis-port=$port --webui-host 0.0.0.0 --num-cpus 1


for host in `uniq $OAR_NODEFILE`; 
do
   	oarsh $host $scripts_home/setup_node.sh $redis_address $flowvr_home; 
done
