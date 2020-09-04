'''
Make sure that ray is exported to your shell
export PATH=$PATH:$HOME/.local/bin
source /home/emorsi/pdi/build/bin/flowvr-suite-config.sh

ray start --head --port=16380 --webui-host 0.0.0.0

flowvr -p tictac
python3 getter.py graphite-1.nancy.grid5000.fr graphite-1.nancy.grid5000.fr

'''

import sys
import time
import ray
from f_proxy import *

if __name__ == '__main__':
    if(len(sys.argv[1:]) < 2):
        print("Invalid cluster arguments")
        exit(1)
    else:
        # precreated ray cluster configuration
        host = sys.argv[1]
        redis = sys.argv[2]

    '''
    Init ray preconfigured cluster
    '''
    ray_init(redis)

    print(ray.available_resources())
  
    port = 'text'
    parent_name = "/".join(["", str(host), "test", "read:P"])
    print(parent_name)

    module_names = ["get", "get1"]
    nCPUs = 2
    f_actor = FlowvrActor.options(num_cpus=nCPUs).remote(port, parent_name)

    f_actor1 = FlowvrActor.options(num_cpus=nCPUs).remote(port, parent_name)

    obj_id = f_actor.exchange_data.remote(module_names[0])
    obj_id1 = f_actor1.exchange_data.remote(module_names[1])

    # obtain results out of all created actors 
    recu_list = ray.get(obj_id)
    recu_list1 = ray.get(obj_id1)

    # do whatever needed with the obtained results 
    # just printing results 
    print(recu_list)
    print(recu_list1)

