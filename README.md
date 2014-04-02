muiltools
=========
A selection of primarily command-line tools often used (atm on linux systems), which I previously maintained with unison (and then Wuala) syncing across systems.

Not everything in the bin directories is my own creation, but the external stuff should be commented as such.

Quick Start
----------
0. `mkdir -p ~/usr && cd ~/usr` (goes to directory where you want to maintain this)
1. `git clone git@github.com:robertmuil/muiltools.git` (clones this repository into it)
2. `cd muiltools && git submodule init` && `git submodule update` (clones all submodules)
2. [optional] `./go` (installs the tools, into `~/usr/local`)

Description
-----------
Under the `bin...` directories are binary files:
`bin` files are for all architectures and so are usually scripts (shell or python)
`bin-x86` files for 32-bit systems
`bin-x64` files for 64-bit systems

Details
-------
A short description of the scripts that I wrote:

* `blank`				- blanks screen with DPMS
* `cameraControl`	- takes a photo using gphoto2 on every keypress

* `consolidate_into`	- moves files from current directory to a target directory, and links are created in the current location

* `dirToFlac`			- converts all mp3 files in cur dir to flac
* `fixMatlab`
* `fixSPSS`

* `installPackage` - these three perform the normal drudgery of configuring and making a tar-ball-type package on a unix type system. Also archives the configured made package to allow uninstallation.
* `archivePackage`
* `uninstallPackage`

* `mresume`   - this is cool: wrapper script for mplayer that automatically bookmarks and resumes
* `menqueue`  - also rather cool even if I say so myself: waits for current mplayer to complete and then plays whatever's on the command line. 
* `makeMovieFromPics`

* `pruneORCSEvo` - cleaning script, very specific to a particular project
* `recoverVim`  - abortive attempt at automating recovery from vim crashes
* `cleanTex`		- removes temp tex files from current directory recursively (up to 2 levels)
* `cleanBak`		- removes backup files, USE CAREFULLY

* `rename-with-date.sh`


* `scrapepicturesfromhtml.bash`

* `setupNewComputer` - this sets up links to point to my config files, which are synced with wuala (not stored here). It also creates the bin-arch link to point to either bin-x86 or bin-64

* `startMatlab`
* `temps` - just monitors temperatures from `sensors` command to command line

* `ddiff` 				- monitors, on stdout, dmesg and other system logs, to allow watching the system state
* `watchForTTYUSB`
* `memWatch`
* `runmon`
