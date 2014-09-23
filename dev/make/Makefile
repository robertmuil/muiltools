DATECOMMAND = `date +%F`
DATESTRING = $(shell date +%F)

blah:
	echo DATECOMMAND=$(DATECOMMAND)
	echo DATESTRING=$(DATESTRING)

dep: this.txt

dep: that.txt
	echo "$(DATESTRING), $^" >> $@

d:=test
SRC := $(wildcard $(d)/*.c) $(wildcard $(d)/*.cpp)

showsrc:
	echo SRC=$(SRC)
