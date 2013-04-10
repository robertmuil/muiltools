#!/bin/bash

htmlfile=$1
urlroot=$2
href='href='
extregex[0]='\.jp\(e\)*g'
extregex[1]='\.gif'
extregex[2]='\.png'
#TODO can only handle one href on a line

#sed -n -e '//p' -e '/href=.*gif/p' -e '/href=.*png/p' ${htmlfile} > ${htmlfile}.piclines
#sed -e 's?.*href="\([^"]*\.jpg\)".*?'${urlroot}'/\1?g' ${htmlfile}.piclines > ${htmlfile}.pics.txt
for ext in ${extregex[@]}; do
	echo "extracting hrefs for '"${ext}"' files..."
	fnames=`sed -n -e 's?.*'${href}'"\([^"]*'${ext}'\)".*?\1?gp' ${htmlfile} |tee ${htmlfile}.stripped_for_${ext}.html`
	for f in ${fnames}; do
		wget "${urlroot}/${f}"
	done
done
