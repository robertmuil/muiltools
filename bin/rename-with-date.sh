#!/bin/bash
shopt -s nullglob #when no matches occur, do nothing.
shopt -s extglob #enable extended patterns in filename expansion (globbing)

LS=/bin/ls

for f in "$@"; do
	#echo "--$f"
	newf=$($LS -l --time-style="+%FT%T" "${f}" |cut -s --output-delimiter='-' -d' ' -f6- )
	#newf=$($LS -l --time-style="+%FT%T" "${f}" |cut -s --output-delimiter='-' -d' ' -f6-|sed -e's/:/./g')
	#echo "---new=[$newf]"
	mv -v "${f}" "${newf}"
done
