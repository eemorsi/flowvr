from sys import argv, exit
import numpy as np
import pdi
import yaml
import ray


if __name__ == '__main__':

    config_path = "get.yml"
    # precreated ray cluster configuration 
    machine = "gros-16"
    cluster = "nancy.grid5000.fr"
    redis = ".".join([machine,cluster])
    ray.init(address=":".join([redis, "16380"]))

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