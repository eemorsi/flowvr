'''
This file is the entry point for the coupled app
Make sure that flowvr and pdi both sourced to the current session

source /home/emorsi/pdi/build/pdi/share/pdi/env.bash
source /home/emorsi/pdi/build/flowvr/bin/flowvr-suite-config.sh

'''

import pdi
import yaml
import ray
import numpy as np
from f_proxy import *
import getter


if __name__ == '__main__':

    if(len(sys.argv[1:]) < 2):
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
    nCPUs = 4
    f_actor = FlowvrActor.options(num_cpus=nCPUs).remote()
    host = ray.get(f_actor.get_root.remote())

    # create flowvr configuration automatically
    app_prefix = create_config(host, frontnode, cluster)
    print("App prefix: {}".format(app_prefix))

    cmd=['flowvr', app_prefix]
    process = Popen(args=" ".join(cmd), stdin=None, stdout=PIPE, stderr=None, shell=True)
    print(process.communicate()[0])

    '''
    Couple C legacy code with python using flowvr
    '''
    # ray.get(  # retrieve results of the running flowvr on a ray actor
    #     f_actor.run.remote(  # run flowvr app
    #         app_prefix
    #     )
    # )
    '''
    Kill the flowvr actor after finish execution
    '''
    # f_actor.kill.remote()
