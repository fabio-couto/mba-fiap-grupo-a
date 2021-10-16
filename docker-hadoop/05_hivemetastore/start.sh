#!/bin/bash
wait.sh hivemetastore_postgres 5432
schematool -dbType postgres -info || schematool -dbType postgres -initSchema

$HIVE_HOME/bin/hive --service metastore