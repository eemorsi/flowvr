#!/bin/bash

dir=$(basename $2)


while inotifywait -r -e modify,create,delete,move $2; 
do
    rsync -avz $2/* $1.g5k:workspace/$dir
done
