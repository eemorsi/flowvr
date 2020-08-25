import pdi
import yaml
import ray
import os
import numpy as np
import sys

from subprocess import PIPE, Popen
from itertools import combinations
from sys import argv, exit


class Resources(object):
    def __init__(self):
        self._nodes = {}
        self.get_resources()

    def get_resources(self):
        for rn in ray.nodes():
            if (rn["Alive"]) and (rn["Resources"]["CPU"] > 1):
                self._nodes[rn["NodeManagerAddress"]] = rn["Resources"]
        return self._nodes

    def get_nodes(self):
        return self._nodes

    def get_hosts(self):
        hosts = []
        for indx, (hostname, cpus) in enumerate(self._nodes.items()):
            [hosts.append(hostname) for _ in range(int(cpus['CPU']))]
        return hosts

    def get_chunk(self, hosts, n):
        for i in range(0, len(hosts), n):
            yield hosts[i:i + n]


'''
FlowVR actor class is responsible for three main functionalities:
    1. Create configuration graph for flowvr 
    2. Allocate resources for the whole run of a flowvr app
    3. Init a run 
'''

@ray.remote
class FlowvrActor(object):
    def __init__(self):
        self.id = 0

    def run(self, f_app_prefix):
        # source= "source /home/emorsi/pdi/build/flowvr/bin/flowvr-suite-config.sh"
        # cmd = ";".join([source, "flowvr"])
        cmd = "flowvr"
        process = Popen(args=" ".join([cmd, f_app_prefix]), stdin=None, stdout=PIPE,
                        stderr=None, shell=True)

        return process.communicate()[0]

    def get_root(self):
        return ray.services.get_node_ip_address()

    '''
    Dumy function -> creat matrix
    '''
    def create_matrix(size):
        return np.random.normal(size=size)
    '''
    Dumy function -> sum of dot product
    '''
    def multiply_matrices(x, y):
        return np.sum(np.dot(x, y))

    '''
    A safe method to clear actorsa
    '''
    def kill(self):
        ray.actor.exit_actor()


def create_config(host, node, cluster):
    from pdi_flowvr import Module_PDI
    from flowvrapp import app, FlowvrRunSSHMultiple

    # can be modified to be dynamic
    # target is to proof it only
    putmodule_cmd = "./cputter"
    getmodule_cmd = " ".join(["python3", "getter.py", str(node), str(cluster)])

    # putrun = FlowvrRunSSHMultiple(putmodule_cmd, hosts=host, prefix="put")
    # getrun = FlowvrRunSSHMultiple(getmodule_cmd, hosts=host, prefix="get")
    putmodule = Module_PDI("put/0", cmdline=putmodule_cmd,
                           pdi_conf="put.yml")  # os.path.join(os.getcwd(),"flowvr/put.yml")
    getmodule = Module_PDI("get/0", cmdline=getmodule_cmd,
                           pdi_conf="get.yml")  # os.path.join(os.getcwd(),"flowvr/get.yml")

    putmodule.getPort("text").link(getmodule.getPort("text"))

    app_prefix = "_".join(["rflowvr", str(host).replace('.','')])
    app.generate_xml(app_prefix)

    return app_prefix


def ray_init(frontnode, cluster):
    redis = ".".join([frontnode, cluster])
    ray.init(address=":".join([redis, "16380"]))
    # ray.init()
