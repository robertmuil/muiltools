muiltools
=========
A selection of primarily command-line tools for linux I often use.

Not everything in the bin directories is my own creation, but everything
that is not mine should be commented as such.

Quick Start
----------
0. Download go script
1. Run it.

Description
-----------
Under the `bin...` directories are binary files:
`bin` files are for all architectures and so are usually scripts (shell or python)
`bin-x86` files for 32-bit systems
`bin-x64` files for 64-bit systems

Details
-------
A short description of the scripts that I wrote:

* `mresume`   - this is cool: wrapper mplayer that bookmarks and resumes play
* `menqueue`  - also rather cool even if I say so myself: waits for current
                mplayer to complete and then plays the given video

* `devdiff`   - monitors dmesg and other system logs, to detected changes

* `memwatch`  - monitor RAM and kill given process if memory gets low to avoid swapping
* `runmon`    - just eval a command and then notify of completion to UI
* `temps`     - just monitors temperatures from `sensors` command

* `watchForTTYUSB`

* `installPackage` - these three perform the normal drudgery of configuring and making a tar-ball-type package on a unix type system. Also archives the configured made package to allow uninstallation.
* `archivePackage`
* `uninstallPackage`

* `blank`				- blanks screen with DPMS
* `cameraControl`	- takes a photo using gphoto2 on every keypress

* `consolidate_into`	- moves files from current directory to a target directory, and links are created in the current location

* `dirToFlac`			- converts all mp3 files in cur dir to flac
* `fixMatlab`
* `startMatlab`
* `fixSPSS`

* `makeMovieFromPics`

* `cleanTex`		- removes temp tex files from current directory recursively (up to 2 levels)
* `cleanBak`		- removes backup files, USE CAREFULLY

* `rename-with-date.sh` - self-explanatory: mainly useful for Photos probably

* `scrapepicturesfromhtml.bash`

* `link_dotfiles` - (formerly setupNewComputer) this sets up links to point to my config files, which are synced with wuala (not stored here). It also creates the bin-arch link to point to either bin-x86 or bin-64
