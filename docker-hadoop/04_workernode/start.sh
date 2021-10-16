#!/bin/bash

wait-namenode.sh
wait-resourcemanager.sh

hdfs --config $HADOOP_CONF_DIR datanode &
yarn --config $HADOOP_CONF_DIR nodemanager &

tail -f /dev/null