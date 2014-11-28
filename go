#!/bin/bash
# This is just a simple script that installs all of the standard
# stuff that I always want on a newly installed linux OS.
set -u
set -e

#TODO: actually determine distro
#TODO: add ubuntu and arch if required
isFedora=1

if [ $isFedora ]; then
	sudo yum update

	sudo yum group install 'C Development Tools and Libraries'
	sudo yum group install 'Development Tools'
	sudo yum install vim-enhanced vim-X11
	sudo yum install zsh

	sudo yum install numpy scipy ipython python-matplotlib
	sudo yum-builddep python-matplotlib
fi

chsh -s $(which zsh)

# Grab my git
# this might be a bit circular because I'll probably store this script in git, but I can at least download it and run it.
mkdir -p ~/usr
pushd ~/usr

if [ ! -d muiltools ]; then
	git clone git@github.com:robertmuil/muiltools.git
	pushd muiltools && git submodule init && git submodule update
else
	pushd muiltools
fi

#Run the setup program to establish links to personal config
./link_dotfiles
./configure_backup

#TODO: these scripts need work
#./fetch_externals && ./do_install
popd
popd
