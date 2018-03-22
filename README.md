## ATTENTION
This software has been abondoned, and is currently not working.
The ffi module for python has not been updated to ZFS 0.7 and is not working correctly
Also the installer is shacky with new Python dependency problems.

TODO before this works:
- Fix build
- Fix Python dependencies (2 -> 3)
- Update libffi or implement JSON ZFS Output bindings

# ZFSmond
Tiny ZFS Web Interface written in AngularJS and Flask Restful

## Compatible Distributions
* [ArchLinux](https://aur.archlinux.org/packages/zfsmond-git/)
* Fedora 21
* Ubuntu 14.04
* OpenSUSE

## Incompatible Distributions (for now)
* Ubuntu 12.04 (too old version of Smartmontools)

## Prerequisites
* ZFS Installed (*NOT* the FUSE module)
* smartmontools installed (i have 6.2 installed)
* GCC
* libffi
* libffi-dev / libffi-devel (Depends on distro)
* libzfs-dev installed
* python-dev / python-devel (Depends on distro)
* Python 2! (3 should work, but some dependancies don't support it)

##Installation:

```bash
git clone https://github.com/FireDrunk/ZFSmond.git zfsmond
pip install -r requirements.txt
pip install git+https://github.com/Xaroth/libzfs-python.git@zpool-config
python main.py
```
Point your browser to: http://[ip]:5000

## Screenshots
https://github.com/FireDrunk/ZFSmond/wiki/Screenshots

## Alpha
Please be aware that this is pre-alpha software!
This software is *NOT* fit for any purpose other than seeing fancy colors!
