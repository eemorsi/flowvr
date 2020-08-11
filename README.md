
## Installation:

 1- FlowVR:	
 ```bash
 git clone https://gitlab.inria.fr/flowvr/flowvr-ex.git
 cd flowvr-ex
 mkdir BUILD
 cd BUILD
 ccmake .. -DCMAKE_INSTALL_PREFIX:PATH=$HOME/pdi/build/flowvr
 make -j
 make install
 ```
 2- PDI:
 ```bash
 source /home/emorsi/pdi/build/flowvr/bin/flowvr-suite-config.sh
 git clone https://gitlab.maisondelasimulation.fr/pdidev/pdi.git
 cd PDI
 mkdir BUILD
 cd BUILD
 cmake -DBUILD_FLOWVR_PLUGIN=ON -DUSE_FlowVR=SYSTEM -DBUILD_PYCALL_PLUGIN=ON -DBUILD_PYTHON=ON -DUSE_HDF5=EMBEDDED -DBUILD_HDF5_PARALLEL=OFF -DBUILD_TESTING=OFF -DCMAKE_INSTALL_PREFIX=$HOME/pdi/build/pdi ..
 make -j
 make Install
 ```

 3- Ray:
 ```bash
 pip3 install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp37-cp37m-manylinux1_x86_64.whl
 
 ```
## Running test:
 1- Make sure that locally installed Ray path is exported to your system path 
 ```bash
 export PATH=$PATH:$HOME/.local/bin
 # For testing 
 Ray start --head --port=123456 
 ```
 2- Start ray cluster after reserving resources by executing
 ```bash
 ./setup_cluster_nodes.sh
 ```
 3- Compile annotated sources after sourcing PDI envirnment variables 
 ```bash
 bash $PDI_HOME/bin/pdirun
 gcc -O2 putter.c -o cputter  -lpdi -lparaconf -lyaml 
 # For testing -> test PDI with empty YAML 
 ./cputter
 ```

## PDI+FlowVR Limitations:
    - PDI is not supported in conda python environments 
    - Langauges bindings e.g. data types support from c <-> python
    - Waiting on data may cause deadline if two-ways data transfere is allowed 
    - PDI's Flowvr documentation is not enough at all to understand how to use FlowVR plugin
    - FlowVR deamon can be hide from the user by providing automatic daemon launcher
    - Duplicate memory sigments can be a limitation factor with a number of applications 
    - 
