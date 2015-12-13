#!/bin/bash
#Author: Robert Muil
shopt -s nullglob #when no matches occur, do nothing.
shopt -s extglob #enable extended patterns in filename expansion (globbing)

LS=/bin/ls

for f in "$@"; do
	if [ -d "$f" ]; then
		echo "skipping dir $f"
		continue
	fi
	#echo "orig:[$f]"
	moddate=$($LS -l --time-style="+%FT%T" "${f}" |cut -s -d' ' -f6)
	newf="$moddate - $f"
	#newf=$($LS -l --time-style="+%FT%T" "${f}" |cut -s --output-delimiter='-' -d' ' -f6-|sed -e's/:/./g')
	#echo "-new:[$newf]"
	mv -v "${f}" "${newf}"
done
