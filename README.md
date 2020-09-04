
## Installation:
 1. SWIG installation for python module API
 ```bash
 # Download SWIG 
 wget https://kumisystems.dl.sourceforge.net/project/swig/swig/swig-4.0.2/swig-4.0.2.tar.gz
 tar -xf swig-4.0.2.tar.gz
 cd swig-4.0.2
 # Configure and install it in a customized directory 
 ./configure --prefix=/home/emorsi/pdi/build
 make -j 
 make install 
 ```

 1. FlowVR:	
 ```bash

 #hint: swig must be exported to allow direct installation of flowvr 
 export PATH=$PATH:/home/emorsi/pdi/build/bin

 # Download the latest version of flowvr 
 git clone https://gitlab.inria.fr/flowvr/flowvr-ex.git
 cd flowvr-ex
 mkdir BUILD
 cd BUILD
 # Configure and install 
 # Without BUILD_FLOWVR_PYTHONMODULEAPI; you will not be able to import flowvr module in python
 ccmake .. -DBUILD_FLOWVR_PYTHONMODULEAPI=ON -DCMAKE_INSTALL_PREFIX:PATH=$HOME/pdi/build
 make -j
 make install
 ```

 2. PDI:
 ```bash
  # Download the latest version of flowvr 
 source /home/emorsi/pdi/build/flowvr/bin/flowvr-suite-config.sh
 git clone https://gitlab.maisondelasimulation.fr/pdidev/pdi.git
 cd PDI
 mkdir BUILD
 cd BUILD
 
  # Configure and install 
 cmake -DBUILD_FLOWVR_PLUGIN=ON -DUSE_FlowVR=SYSTEM -DBUILD_PYCALL_PLUGIN=ON -DBUILD_PYTHON=ON -DUSE_HDF5=EMBEDDED -DBUILD_HDF5_PARALLEL=OFF -DBUILD_TESTING=OFF -DCMAKE_INSTALL_PREFIX=$HOME/pdi/build ..
 make -j
 make Install
 ```

 3. Ray:
 ```bash
 pip3 install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp37-cp37m-manylinux1_x86_64.whl
 
 ```
## Running test:
 1. Make sure that locally installed Ray path is exported to your system path 
 ```bash
 export PATH=$PATH:$HOME/.local/bin
 # For testing 
 Ray start --head --port=123456 
 ```
 2. Start ray cluster after reserving resources by executing
 ```bash
 ./setup_cluster_nodes.sh
 ```
 3. Compile annotated sources after sourcing PDI envirnment variables 
 ```bash
 bash $PDI_HOME/bin/pdirun
 gcc -O2 putter.c -o cputter  -lpdi -lparaconf -lyaml 
 # For testing -> test PDI with empty YAML 
 ./cputter
 ```

## PDI+FlowVR Limitations:
    - PDI is not supported in conda python environments so inorder to allowing coupling of the FlowVR though PDI; all packages have be install to the system or locally exported to the system path 
    - Only a few primitive datatypes are allowed between different langauges e.g.  string datatype not support from c <-> python
    - PDI wait_on_data may cause deadline if two-ways data transfere is allowed or in other words if each module contains input and output ports. In this case a presegnal is required to end deadlock on wait
    - PDI's Flowvr documentation is not enough at all to understand how to use FlowVR plugin
    - FlowVR deamon can be hide from the user by providing automatic daemon launcher
    - Duplicate memory sigments can be a limitation factor with a number of applications  
