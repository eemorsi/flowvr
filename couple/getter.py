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


@ray.remote
class FlowvrActor(object):
    def __init__(self, port, ports, parent_name):
        self.port, self.ports, self.parent_name = port, ports, parent_name

    def exchange_data(self, module_name):
        module = flowvr.initModule(
            self.ports, "", str(module_name), self.parent_name)
        recu_list = []

        while module.wait():
            message = self.port.get()
            # print("get receives {} at it {}".format(message.data.asString().decode(), message.getStamp("it")))
            recu_list.append(message.data.asString().decode())
        return module, recu_list

    def close(self, module):
        module.close()
        ray.actor.exit_actor()


if __name__ == '__main__':
    if(len(sys.argv[1:]) < 3):
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
    ports = flowvr.vectorPort()
    port = flowvr.InputPort('text')
    ports.push_back(port)
    parent_name = "/".join(["", str(host), "test", "read:P"])
    print(parent_name)

    module_names = ["get", "get1"]
    nCPUs = 2
    f_actor = FlowvrActor.options(
        num_cpus=nCPUs).remote(port, ports, parent_name)

    f_actor1 = FlowvrActor.options(
        num_cpus=nCPUs).remote(port, ports, parent_name)

    obj_id = f_actor.exchange_data.remote(module_names[0])
    obj_id1 = f_actor.exchange_data.remote(module_names[1])

    module, recu_list = ray.get(obj_id)
    module1, recu_list1 = ray.get(obj_id1)

    print(recu_list)
    print(recu_list1)

    # module = flowvr.initModule(ports,"",str(module_name),parent_name)

    # while module.wait():
    #   message = port.get()
    #   print("get receives {} at it {}".format(message.data.asString().decode(), message.getStamp("it")))

    # module.close()
