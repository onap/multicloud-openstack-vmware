#!/bin/bash -v

cd ./vio
./run.sh

while [ ! -f logs/runtime_vio.log ]; do
    sleep 1
done
tail -F logs/runtime_vio.log
