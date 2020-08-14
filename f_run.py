import pdi
import yaml
import ray
# import os
import numpy as np
# import sys

# from subprocess import PIPE, Popen
# from itertools import combinations
# from sys import argv, exit
from f_proxy import *
import getter


if __name__ == '__main__':

    if(len(sys.argv[1:])< 2):
        print("Invalid cluster arguments")
        exit(1)
    else:
        
        # precreated ray cluster configuration
        frontnode = sys.argv[1] 
        cluster = sys.argv[2] 

    '''
    Init ray preconfigured cluster
    '''
    ray_init(frontnode, cluster)
    '''
    - Retrieve lists of hosts for locating processes
    - The List of resources can be manually used for forcing run of the simulator 
        but allocated resources for this case won't be seen by Ray 
    '''
    # cluster = Resources()
    # hosts = cluster.get_hosts()
    # print(hosts)

    '''
    Handle resources for FlowVR app and proxy
    nCPUs is the total number of cores required for running proxy functions and the simulator
    '''
    nCPUs=4
    f_actor= FlowvrActor.options(num_cpus=nCPUs).remote()
    host = ray.get(f_actor.get_root.remote())
    
    f_app_prefix = create_config(host, frontnode, cluster)
    print(f_app_prefix)

    '''
    Start data exchange with flowvr
    '''
    ray.get(f_actor.run.remote(" ".join(["flowvr", f_app_prefix])))
    '''
    Kill the flowvr actor after finish execution
    '''
    f_actor.kill.remote()