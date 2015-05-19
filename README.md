# ZFSmond
Tiny ZFS Web Interface written in AngularJS and Flask Restful

## Compatible Distributions
* Fedora 21
* Ubuntu 14.04
* OpenSUSE

## Incompatible Distributions (for now)
* ArchLinux (comes with Python3 by default)
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
git clone https://github.com/Xaroth/libzfs-python.git libzfs-python
cd zfsmond
ln -s ../libzfs-python/libzfs/ libzfs
pip install -r requirements.txt
python main.py
```
Point your browser to: http://[ip]:5000

## Screenshots
https://github.com/FireDrunk/ZFSmond/wiki/Screenshots

## Alpha
Please be aware that this is pre-alpha software!
This software is *NOT* fit for any purpose other than seeing fancy colors!
