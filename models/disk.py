import os
import subprocess
import pyudev
from pySMART import Device
from flask.ext import restful

class Disk(restful.Resource):
	def get(self):
		return disk_list()


#
# TODO: Migrate to inner class functions
#

def get_block_device_size(device):
	if not device:
		return 0
	try:
		return subprocess.check_output(['blockdev','--getsize64', device])
	except:
		return 0

def disk_list():
	disks = []

	context = pyudev.Context()
	for device in context.list_devices(subsystem="block"):
		if device.device_type == u"disk":
			property_dict = dict(device.items())

			if ('ID_MODEL' in property_dict):
				disk_short_name = property_dict.get('DEVNAME', "Unknown").split('/')[-1]
				disks.append(
				{
					'model':	property_dict.get('ID_MODEL', "Unknown"),
					'name':		disk_short_name,
					'size':		get_block_device_size(property_dict.get('DEVNAME', None)),
					'serial':	property_dict.get('ID_SERIAL_SHORT', "Unknown"),
				})

	return disks
