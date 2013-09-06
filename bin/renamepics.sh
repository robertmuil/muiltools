#!/bin/bash
#
# Renames pictures in directory based on Pic date.

dirtoprocess=./

BASE="$HOME/Pictures/test"

exiftool -v -d "${BASE}/%Y/%Y-%m-%d" "-directory<DateTimeOriginal" $dirtoprocess
