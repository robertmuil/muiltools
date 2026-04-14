#!/usr/bin/env bash

host=$1

DATE="date +%Y-%m-%dT%H:%M:%S"

if [ -z "$host" ]; then
	echo "provide host"
	exit 1
fi


while true; do
	printf "\n\n>>> $($DATE): "
	ping -c 5 -A "$host"
	sleep 2.0
done
