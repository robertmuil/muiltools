#!/bin/bash
#
# Bit of a hack to implement certain fixes to common SVG problems, typically caused
# with PDF conversions.
# ATM, only fix is of specification of individual letters inside a text span.
# NB: this just removes the individual x positions. Should really calculate the desired letter spacing and change to that. But that's hard.
# robertmuil

op='fixed-letter-spacing'

for f in "$@"; do
	tmpf=.$f.tmp
	oldf=$f.bak
	if [ -e $oldf ]; then
		echo "Error: '$oldf' already exists. Cowardly exiting."
		exit 2
	fi
	/bin/cp "$f" "$oldf"
	if [ X$op == X"fixed-letter-spacing" ]; then
		echo "Looking for fixed letter spacing..."
		sed -e 's/x=\"\([0-9.]\+\)\( [0-9.]*\)\+\"/x=\"\1\"/g' "$oldf" > "$f"
		diff "$oldf" "$f"
	fi
done
