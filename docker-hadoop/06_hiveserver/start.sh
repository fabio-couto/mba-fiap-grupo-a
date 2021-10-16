#!/bin/bash

wait-namenode.sh
wait-resourcemanager.sh
wait.sh hivemetastore 9083

hadoop fs -mkdir       /tmp
hadoop fs -mkdir -p    /user/hive/warehouse
hadoop fs -chmod g+w   /tmp
hadoop fs -chmod g+w   /user/hive/warehouse

$HIVE_HOME/bin/hive --service hiveserver2