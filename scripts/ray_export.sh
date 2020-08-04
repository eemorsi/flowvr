#!/bin/bash 


source /home/emorsi/.bazel/bin/bazel-complete.bash
export PATH=$PATH:/home/emorsi/bin


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/emorsi/ray/bazel-out/k8-opt/bin:/home/emorsi/ray/bazel-out/k8-opt/bin/cpp
