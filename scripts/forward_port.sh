#!/bin/bash

kill -9 $(ps aux|grep 38888|awk '{print $2}')
kill -9 $(ps aux|grep 38265|awk '{print $2}')

ssh -N -f -L 38888:$1:8768 $2.g5k
ssh -N -f -L 38265:$1:8265 $2.g5k


