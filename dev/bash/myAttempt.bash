#!/bin/bash

level1dirs="fs21 fs22 fs23 fs24"
level2dirs="pre post"
level3dirs="localizer blah bling"

for l1 in $level1dirs; do
	for l2 in $level2dirs; do
		for l3 in $level3dirs; do
			mkdir -vp $l1/$l2/$l3
		done
	done
done
echo "done"

