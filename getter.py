import pdi
import yaml
import ray
import os
import numpy as np

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
class Actor(object):
    def __init__(self):
        self.id = 0

    def run(self, cmd, hosts):
        process = Popen(args=cmd, stdin=None, stdout=PIPE,
                        stderr=None, shell=True)
        return process.communicate()[0]

    def get_root(self):
        return ray.services.get_node_ip_address()

    # A safe method to clear actors
    def kill(self):
        ray.actor.exit_actor()

# class FlowvrActor(Actor):
#     def run(self, cmd, hosts):



if __name__ == '__main__':

    # precreated ray cluster configuration
    machine = "gros-16"
    cluster = "nancy.grid5000.fr"
    redis = ".".join([machine, cluster])
    ray.init(address=":".join([redis, "16380"]))
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

        print("PY scalar: {}".format(scalar))
        pdi.expose('wait', wait, pdi.IN)

    pdi.finalize()
