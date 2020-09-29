#!/usr/bin/env bash

host=$1

DATE="date +%Y-%m-%dT%H:%M:%S"

if [ -z "$host" ]; then
	echo "provide host"
	exit 1
fi


while true; do
	printf "\n\n>>> $($DATE): "
	ping -c 2 -A "$host"
	sleep 0.2
done
