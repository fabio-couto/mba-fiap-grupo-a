#!/bin/bash

wait-namenode.sh
wait-resourcemanager.sh
wait.sh zookeeper.hadoop 2181 

flume-ng agent -n flume1 -c conf -f /opt/flume/conf/flume.conf — Dflume.root.logger=INFO,console