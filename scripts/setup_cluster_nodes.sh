#!/bin/bash
source /etc/profile
module load miniconda3/4.5.11_gcc-6.4.0
source activate rllibd

port=16380
redis_address="$(hostname --ip-address)"
redis_address="$redis_address:$port"

pdi_home=$HOME/pdi/build
scripts_home=`pwd`

ray start --head --redis-port=$port --webui-host 0.0.0.0 --num-cpus 1


for host in `uniq $OAR_NODEFILE`; 
do
   	oarsh $host $scripts_home/setup_node.sh $redis_address $pdi_home; 
done
