import ray
import os
import numpy as np
import sys
import flowvr

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
    def __init__(self, port, parent_name):
        self.port_n, self.parent_name = port, parent_name

    def exchange_data(self, module_name):
        
        ports = flowvr.vectorPort()
        port = flowvr.InputPort(self.port_n)
        ports.push_back(port)

        module = flowvr.initModule(ports , "", str(module_name), self.parent_name)
        recu_list = []

        while module.wait():
            message = port.get()
            # print("get receives {} at it {}".format(message.data.asString().decode(), message.getStamp("it")))
            recu_list.append(message.data.asString().decode())
        
        module.abort()
        module.close()

        return recu_list

    def close(self):
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


def ray_init(redis):
    # redis = ".".join([frontnode, cluster])
    ray.init(address=":".join([redis, "16380"]))
    # ray.init()
