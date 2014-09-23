#!/bin/bash
shopt -s extglob
regExWhitespace="[ \t\r\n\v\f]"
lineRegex="^([0-9]+)$regExWhitespace+(.*)"
while read line; do

	if [[ "${line}" =~ $lineRegex ]]; then
	 size=${BASH_REMATCH[1]}
	 fName=${BASH_REMATCH[2]}
	 echo " - '${fName}' (${size} bytes)"
 else
	 echo " line ignored"
 fi
done
