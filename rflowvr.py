from flowvrapp import *
from pdi_flowvr import Module_PDI

putmodule = Module_PDI("put", cmdline = "./putter", pdi_conf = "put.yml")
getmodule = Module_PDI("get", cmdline = "python getter.py", pdi_conf = "get.yml")

putmodule.getPort("text").link(getmodule.getPort("text"))
        
app.generate_xml("rflowvr")
