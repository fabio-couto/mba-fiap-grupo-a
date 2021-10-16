#!/bin/bash
host=$1
port=$2
ready=0
while [ $ready -eq 0 ]
do
	nc -z $host $port
	if [ $? -eq 0 ]; then
		echo "$host is ready..."
		ready=1
	else
		echo "Waiting $host to be ready..."
		sleep 3
	fi
done