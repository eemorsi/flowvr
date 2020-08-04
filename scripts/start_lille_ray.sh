#/bin/sh

port=16380
redis_address=lille
redis_address="$redis_address:$port"
for host in `uniq $OAR_NODEFILE`; do
    oarsh $host ./setup_node.sh $redis_address
done



