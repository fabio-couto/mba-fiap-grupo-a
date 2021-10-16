#!/bin/bash

wait-namenode.sh
wait-resourcemanager.sh

/opt/livy/bin/livy-server start
tail -f /dev/null