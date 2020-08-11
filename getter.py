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


@ray.remote
class FlowvrActor(object):
    def __init__(self, id):
        self.id = id

    def run(self, cmd, hosts):
        process = Popen(args=cmd, stdin=None, stdout=PIPE,
                        stderr=None, shell=True)
        return process.communicate()[0]

    def get_root(self):
        return ray.services.get_node_ip_address()

    def create_config(self, hosts, node, cluster):
        from flowvrapp import *
        from pdi_flowvr import Module_PDI

        # can be modified to be dynamic 
        # target is to proof it only 
        putmodule_cmd="./cputter"
        getmodule_cmd=" ".join(["python3","getter.py",node, cluster])

        putmodule = Module_PDI("put", cmdline = putmodule_cmd, pdi_conf = "put.yml")
        getmodule = Module_PDI("get", cmdline = getmodule_cmd, pdi_conf = "get.yml")

        putmodule.getPort("text").link(getmodule.getPort("text"))
                
        app.generate_xml("rflowvr")

    # A safe method to clear actors
    def kill(self):
        ray.actor.exit_actor()


def ray_init():
    if(len(sys.argv[1:])< 2):
        print("Invalid cluster arguments")
        exit(1)
    else:
        
        # precreated ray cluster configuration
        machine = sys.argv[1] # "grisu-48"
        cluster = sys.argv[2] # "nancy.grid5000.fr"
        redis = ".".join([machine, cluster])
        ray.init(address=":".join([redis, "16480"])) 
        # ray.init()




if __name__ == '__main__':
    '''
    Init ray preconfigured cluster
    '''
    ray_init()
    '''
    Retrieve lists of hosts for locating processes
    '''
    cluster = Resources()
    hosts = cluster.get_hosts()
    print(hosts)

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

    pdi.expose('wait', wait, pdi.IN)
    # with each message passed through flowvr, create an actor job
    while(wait != 0):
        pdi.expose('scalar', scalar, pdi.IN)
        # Dumy Ray computation and sum 
        
        print("PY scalar: {}".format(scalar))
        pdi.expose('wait', wait, pdi.IN)

    pdi.finalize()
