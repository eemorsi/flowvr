import sys, time
import flowvr

if __name__ == '__main__':
  ports = flowvr.vectorPort()
  port = flowvr.InputPort('text')
  ports.push_back(port)
  module = flowvr.initModule(ports);
  
  while module.wait():
    message = port.get()   
    print("get receives {} at it {}".format(message.data.asString().decode(), message.getStamp("it")))


  module.close()