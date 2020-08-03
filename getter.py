from sys import argv, exit
import numpy as np
import pdi
import yaml


if __name__ == '__main__':

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
    while(wait != 0):
        pdi.expose('scalar', scalar, pdi.IN)
        print("PY scalar: {}".format(scalar))
        pdi.expose('wait', wait, pdi.IN)

    pdi.finalize()