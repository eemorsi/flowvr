import sys, time
import flowvr

class Flowvr(object):
  def __init__(self, ports, parent_name):
    module = flowvr.initModule(ports,"",str(module_name),parent_name)
    return module
  
  def exchange_data(self, port):
    recu_list=[]
    while module.wait():
      message = port.get()   
      # print("get receives {} at it {}".format(message.data.asString().decode(), message.getStamp("it")))
      recu_list.append(message.data.asString().decode())
    return recu_list

  def close(self, module):
    module.close()



if __name__ == '__main__':
  if(len(sys.argv[1:]) < 2):
      print("Invalid cluster arguments")
      exit(1)
  else:
      # precreated ray cluster configuration
      module_name = sys.argv[1]
      host = sys.argv[2]  

  ports = flowvr.vectorPort()
  port = flowvr.InputPort('text')
  ports.push_back(port)
  parent_name="/".join(["",str(host),"test","read:P"])
  print(parent_name)
  
  # module = flowvr.initModule(ports,"",str(module_name),parent_name)
  
  # while module.wait():
  #   message = port.get()   
  #   print("get receives {} at it {}".format(message.data.asString().decode(), message.getStamp("it")))


  # module.close()