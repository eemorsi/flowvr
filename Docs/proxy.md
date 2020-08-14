** Possible workflow/script for starting a coupled flowvr/ray app. 
 1. Get a list of hosts from batch scheduler: OARlist
 2. Identify a frontnode that could be either one of the OARList or the current frontnode of the
    computer. Will be used to run Ray frontend and flowvr frontend.
 3. ~~From this list build 3 lists:  
    - AppList: nodes to run the application
    - ProxyList: nodes where to run the flowvr/ray proxy. If going in situ (proxies running on same
      nodes than flowvr application) the this list will likely    be a sub list of AppList
    - RayList: resources that will use Ray for running workers (do not include the ProxyList)~~\
 <mark> Allow Ray to manage all resources as a single pool of machines, each entity can be use then either for doing compution as a ray actor or simply for the simulator</mark>
 4. Flowvr app description get the 2 first lists to instantiate the graph. The proxy are included
    but without starting command (use ":" instead)
    - python3 app.py AppList ProxyList
 5. flowvrdList: union of AppList and ProxyList removing duplicates
 6. Start daemons on frontnode + flowvrdList. Use either flowvr-run-ssh or mpirun as launcher
    - mpirun --hosts frontnode+flowvrList flowvrd 
    - flowvr-run-ssh frontnode+flowvrList flowvrd
 7. Start the flowvr application from the frontNode
    - flowvr -a  app
 8. Start Ray (redis data base) and add all nodes of  RayList and ProxyList.
    - you know better than me how to do this
 9. Start a Ray script that:
    - start the proxies actors on the nodes of the ProxyList. These actors implement flowvr modules
      and so once started they will connect to their local flowvrd. Need to forward the FLOWVR
      specific env variables (exemple: flowvr-run-ssh -e FLOWVR_MODNAME "get" -e FLOWVR_PARENT
      "/machine1/read:P"  -v  ' localhost ' python tictac_module.py get, but work with any launcher
      as long as there is a way to forward an ENV variable)
    - start some ray tasks that will call a "getmessage" methods from the proxy actors to retrieve
      the last message the proxy received from the app. This   get method will basically execute a flowvr wait then a flowvr
      get and next return the received message that will be moved  through Ray to the caller. Note
      that the flowvr wait does not have to be in a loop. It can perfectly be in a getmessage
      method  executed each time this method is being called. 
      
 10. Reading and writting data to the app through the proxy. They are various options there. The
     simplest is to have in the proxy input and output ports and a getmessage and putmessage method
     that each make a call to the wait and them make the necessary put/get. Be careful that when
     you make a put the put is actually performed in the next wait call, while when you make a get
     you need first to make a wait to get access to the last message in the queue or wait for it if
     the last one received has already been consumed through a previous wait/get (and the message
     is them suppressed). Other options are:
     1. Have 2 proxies modules , one for reading and one for    writing.
     2. Have 2  modules in one proxy. This  is actually doable. It is perfectly  possible to declare
        two modules into one process. These modules do not have to run in separate threads (they can
        of course). So in that case you would  have an actor with a getmessage and putmessage method
        each method referring  to a different module. This  is a little more tricky  to program this
        way  as not  properly  documented.   An example  is  the flowvr  command  used  to start  an
        application that  actually starts  two local  modules read and  send (but this is not a
        trivial code).  read  runs in  its own thread (ctrlin with  a quite traditional wait loop)
        while the send run in  the main process   with a wait that is called each one a new command
        needs to be executed (so for instance when   the user type on the console a 'stop'). So
        this look much like the putmessage method we are talking about here:
        - https://gitlab.inria.fr/flowvr/flowvr-ex/-/blob/1679840de59fe7c41b7c0db694c46bc8555e5db0/flowvr/flowvr-daemon/include/flowvr/telnet.h
        - https://gitlab.inria.fr/flowvr/flowvr-ex/-/blob/master/flowvr/flowvr-daemon/src/utils/telnet.cpp
          
     
