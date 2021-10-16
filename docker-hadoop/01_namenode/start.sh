#!/bin/bash
if [ ! -e "/hadoop/dfs/name/current" ]; then
    hdfs namenode -format
fi

hdfs namenode