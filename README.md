muiltools
=========
A selection of primarily command-line tools often used (atm on linux systems), which I previously maintained with unison (and then Wuala) syncing across systems.

Quick Start
----------
0. `mkdir -p ~/usr && cd ~/usr` (goes to directory where you want to maintain this)
1. `git clone git@github.com:robertmuil/muiltools.git` (clones this repository into it)
2. `cd muiltools && git submodule init` && `git submodules update` (clones all submodules)
2. [optional] `./go` (installs the tools, into `~/usr/local`)

Description
-----------
Under the `bin...` directories are binary files:
`bin` files are for all architectures and so are usually scripts (shell or python)
`bin-x86` files for 32-bit systems
`bin-x64` files for 64-bit systems

Details
-------
Here's some notes of scripts I've written here.

* `blank`				- blanks screen with DPMS
* `cameraControl`	- takes a photo using gphoto2 on every keypress


* `consolidate_into`	- moves files from current directory to a target directory, and links are created in the current location

* `dirToFlac`			- converts all mp3 files in cur dir to flac
* `fixMatlab`
* `fixSPSS`

* `installPackage`
* `archivePackage`
* `uninstallPackage`

* `menqueue`
* `mresume`   - this is cool: wrapper script for mplayer that automatically bookmarks and resumes
* `makeMovieFromPics`

* `pruneORCSEvo`
* `recoverVim`  - abortive attempt at automating recovery from vim crashes
* `cleanTex`  		- removes temp tex files from current directory recursively (up to 2 levels)
* `rename-with-date.sh`


* `scrapepicturesfromhtml.bash`

* `startMatlab`
* `temps` - just monitors temperatures from `sensors` command to command line

* `ddiff` 				- monitors, on stdout, dmesg and other system logs, to allow watching the system state
* `watchForTTYUSB`
* `memWatch`
* `runmon`
