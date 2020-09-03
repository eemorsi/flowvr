'''
Make sure that ray is exported to your shell 
export PATH=$PATH:$HOME/.local/bin

source /home/emorsi/pdi/build/bin/flowvr-suite-config.sh
export PATH=$PATH:/home/emorsi/.local/bin

python3 getter.py get1 grisou-9.nancy.grid5000.fr grisou-9.nancy.grid5000.fr

'''
import sys
import time
import flowvr
import ray
from f_proxy import *

if __name__ == '__main__':
    '''
    Check the parameters passed to the getter ... 
    '''
    if(len(sys.argv[1:]) < 3):
        print("Invalid cluster arguments")
        exit(1)
    else:
        # Precreated ray cluster configuration
        module_name = sys.argv[1]
        host = sys.argv[2]
        # Configuration parameters for ray
        redis = sys.argv[3]

    '''
  Init ray preconfigured cluster
  '''
    ray_init(redis)
    print(ray.available_resources())

    '''
  Set flowvr ports 
  '''
    ports = flowvr.vectorPort()
    port = flowvr.InputPort('text')
    ports.push_back(port)
    parent_name = "/".join(["", str(host), "test", "read:P"])
    print(parent_name)

    module = flowvr.initModule(ports, "", str(module_name), parent_name)

    # define the number of cores required for single computation
    nCPUs = 2
    # holders of the ray elemenets

    z_ids = []
    indx = 0
    f_actors = []

    while (module.wait()):
        message = port.get()
        print("get receives size of {} at it {}".format(
            message.data.asString().decode(), message.getStamp("it")))
        size = int(message.data.asString().decode())

        # Dumy Ray computation and sum
        f_actor = FlowvrActor.options(num_cpus=nCPUs).remote()
        f_actors.append(f_actor)

        x_id = f_actor.create_matrix.remote([size, size])
        y_id = f_actor.create_matrix.remote([size, size])
        z_ids.append(f_actor.multiply_matrices.remote(x_id, y_id))

    print(z_ids)

    # retreive results computed by ray
    results = [ray.get(z_obj_id) for z_obj_id in z_ids]
    print(results)

    [a.kill.remote() for a in f_actors]
    module.close()
