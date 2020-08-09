
## Installation:
 1- FlowVR:	\
 git clone flowvr-ex\
 ccmake .. -DCMAKE_INSTALL_PREFIX:PATH=$HOME/pdi/build/flowvr\
 make -j\
 make install

 2- PDI:
 
 source /home/emorsi/pdi/build/flowvr/bin/flowvr-suite-config.sh\
 git clone PDI\
 cd PDI\
 mkdir BUILD; cd BUILD\
 cmake -DBUILD_FLOWVR_PLUGIN=ON -DUSE_FlowVR=SYSTEM -DBUILD_PYCALL_PLUGIN=ON -DBUILD_PYTHON=ON -DUSE_HDF5=EMBEDDED -DBUILD_HDF5_PARALLEL=OFF -DBUILD_TESTING=OFF -DCMAKE_INSTALL_PREFIX=$HOME/pdi/build/pdi ..\
 make -j\
 make Install\

 3- Ray:

 pip3 install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp37-cp37m-manylinux1_x86_64.whl\
 export PATH=$PATH:$HOME/.local/bin

 4- Start ray cluster after reserving resources by executing\
 ./setup_cluster_nodes.sh
 
## PDI+FlowVR Limitations:
1- Langauges bindings e.g. data types support from c <-> python
