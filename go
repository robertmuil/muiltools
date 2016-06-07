#!/bin/bash
#This is a bootstrapping script - just installs a bare minimum in order to get git, then get the repo of which this is a part, then can call the full update script
set -u
set -e

if $(which git &> /dev/null); then
	echo "got git, proceeding..."
else
	#Duck-typing: try apt-get and if it works use it...
	if $(which apt-get &> /dev/null); then
		sudo apt-get install git
	elif $(which dnf &> /dev/null); then
		sudo dnf install git
	elif $(which yum &> /dev/null); then
		sudo yum install git
	else
		echo "Only support apt-get, dnf and yum so far, sorry... try installing git manually."
		exit 1
	fi
fi

# Grab my git in case it's not already there.
mkdir -p ~/usr
pushd ~/usr

if [ ! -d muiltools ]; then
	echo "Going to clone muiltools from GitHub now. You will be prompted for a password if you don't have your SSH key from this machine in GitHub (you can do that now if you want)... press enter when you're ready... (ctrl-c to quit)"
	read
	git clone git@github.com:robertmuil/muiltools.git
	pushd muiltools && git submodule init && git submodule update
else
	pushd muiltools
	git pull
fi

#Start the full muiltools install
./do_install

popd
popd
