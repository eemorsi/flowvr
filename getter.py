import pdi
import yaml
import ray
import numpy as np
from f_proxy import *


'''
Dumy function -> creat matrix
'''
@ray.remote
def create_matrix(size):
    return np.random.normal(size=size)
'''
Dumy function -> sum of dot product
'''
@ray.remote
def multiply_matrices(x, y):
    return np.sum(np.dot(x, y))



if __name__ == '__main__':

    if(len(sys.argv[1:])< 2):
        print("Invalid cluster arguments")
        exit(1)
    else:
        frontnode = sys.argv[1] 
        cluster = sys.argv[2] 

    '''
    Init ray preconfigured cluster
    '''
    ray_init(frontnode, cluster)
    print(ray.available_resources())
   
    '''
    nCPUs is the number of cores required for running only the Ray actors 
    '''
    nCPUs=2
    # f_actor= FlowvrActor.options(num_cpus=nCPUs).remote()
    # host = ray.get(f_actor.get_root.remote())
    
    '''
    Start data exchange with flowvr
    '''
    config_path = "get.yml"
    with open(config_path, 'r') as config_file:
        try:
            config = yaml.load(config_file)
        except yaml.YAMLError as exc:
            exit(exc)

    pdi.init(yaml.dump(config["pdi"]))
    wait = np.array(0)
    scalar = np.array(0)


    size = 10
    # z_ids = [1]*size
    z_ids=[]
    indx=0
    f_actors=[]
    pdi.expose('wait', wait, pdi.IN)
    # with each message passed through flowvr, create an actor job
    while(wait != 0):
        pdi.expose('scalar', scalar, pdi.IN)

        # Dumy Ray computation and sum 
        f_actor = FlowvrActor.options(num_cpus=nCPUs).remote()
        f_actors.append(f_actor)
        # f_actors.append( FlowvrActor.options(num_cpus=nCPUs).remote())
        # f_actor = f_actors[indx]
        # indx+=1

        x_id = f_actor.create_matrix.remote([scalar, scalar])
        y_id = f_actor.create_matrix.remote([scalar, scalar])
        z_ids.append(f_actor.multiply_matrices.remote(x_id, y_id))

        print("PY scalar: {}".format(scalar))
        print("wait before: {}".format(wait))
        pdi.expose('wait', wait, pdi.IN)
        print("wait after: {}".format(wait))
    '''
    Compute the result out of all ray calls 
    '''
    print(z_ids)
    
    results = [ray.get(z_obj_id) for z_obj_id in z_ids]

    """
    Kill actors to release resoucres of workers
    """
    # [a.kill.remote() for a in f_actors]
    print(results)

    '''
    Finalize data exchange and kill active actor from Ray 
    '''
    pdi.finalize()
    # f_actor.kill.remote()