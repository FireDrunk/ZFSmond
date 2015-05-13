# ZFSmond
Tiny ZFS Web Interface written in AngularJS and Flask Restful

## Prerequisites
*ZFS Installed
*Smartmontools installed
*libzfs-dev installed
*Python 2! (3 should work, but some dependancies don't support it)

##Installation:

```bash
git clone https://github.com/FireDrunk/ZFSmond.git zfsmond
git clone https://github.com/Xaroth/libzfs-python.git libzfs-python
cd zfsmond
ln -s libzfs ../libzfs-python/libzfs
pip install -r requirements.txt
python main.py
```
Point your browser to: http://[ip]:5000

## Alpha
Please be aware that this is pre-alpha software!
This software is *NOT* fit for any purpose other than seeing fancy colors!
