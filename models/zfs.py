from libzfs import *
from libzfs.zpool import *
from libzfs.zdataset import *
from libzfs.utils.jsonify import *
from flask.ext import restful
import time

class Pool(restful.Resource):
	def get(self):
		pools = []
		for raw_pool in ZPool.list():
			pool_info = {}
			pool_info['name'] = raw_pool.name
			pool_info['state'] = zpool_state_to_str(raw_pool.state)
			pool_info['status'] = zpool_status_to_str(raw_pool.status)
			pool_info['size'] = raw_pool.properties[zpool_prop_t.ZPOOL_PROP_SIZE]
			pool_info['allocated'] = raw_pool.properties[zpool_prop_t.ZPOOL_PROP_ALLOCATED]
			pool_info['capacity'] = raw_pool.properties[zpool_prop_t.ZPOOL_PROP_CAPACITY]
			pool_info['free'] = raw_pool.properties[zpool_prop_t.ZPOOL_PROP_FREE]
			pool_info['isok'] = (pool_info['status'] == "Ok")
			pool_info['config'] = self.generate_config(raw_pool)

			pools.append(pool_info)
		return pools

	def generate_config(self, pool):
		config = {}
		#config['raw'] = pool.config
		config['guid'] = pool.config.guid
		config['scrub'] = pool.config.vdev_tree.scan_stats

		#config['raw'] = pool.config
		nr_of_vdevs = len(pool.config.vdev_tree.children)

		config['nr_of_vdevs'] = nr_of_vdevs

		vdevs = []
		for vdev_config in pool.config.vdev_tree.children:
			# Skip weird vdev types
			if vdev_config.type == 'hole':
				continue

			# Test if the VDEV has children
			vdev_children = []
			if vdev_config.children:
				for child in vdev_config.children:
					vdev_children.append({
							'type': child.type,
							'path': child.path,
							'name': ''.join(child.path.split('/')[-1]),
							'vdev_stats': jsonify(child.vdev_stats, parse_enums=PARSE_BOTH)
					})
			else:
				vdev_children.append({
						'type': vdev_config.type,
						'path': vdev_config.path,
						'name': ''.join(vdev_config.path.split('/')[-1]),
						'vdev_stats': jsonify(vdev_config.vdev_stats, parse_enums=PARSE_BOTH)
				})

			vdevs.append({
				'ashift' : vdev_config.ashift,
				'nparity' : vdev_config.nparity,
				'type' : vdev_config.type,
				'vdev_stats': jsonify(vdev_config.vdev_stats, parse_enums=PARSE_BOTH),
				'children' : vdev_children
			})

		config['vdevs'] = vdevs

		return config

class Filesystem(restful.Resource):
	def get(self):
		pools = []
		for pool in ZPool.list():
			fs = []
			root_fs = ZDataset.get(pool.name)

			# Append the root filesystem
			root_fs._properties = jsonify(root_fs.properties)

			fs.append(
				{
					'name' : root_fs.name,
					'available' : root_fs.properties['available'],
					'referenced' : root_fs.properties['referenced'],
					'used' : root_fs.properties['used'],
				})

			for sub_fs in root_fs.child_filesystems:
				# Snapshots
				snaps = []
				for sub_snap in sub_fs.child_snapshots:
					sub_snap._properties = jsonify(sub_snap.properties)

					snaps.append(
						{
							'name' : sub_snap.name,
							'referenced' : sub_snap.properties['referenced'],
							'used' : sub_snap.properties['used'],
						})
				sub_fs._properties = jsonify(sub_fs.properties)

				fs.append(
					{
						'name' : sub_fs.name,
						'available' : sub_fs.properties['available'],
						'referenced' : sub_fs.properties['referenced'],
						'used' : sub_fs.properties['used'],
						'snaps' : snaps
					})
			pools.append({
				'name' : pool.name,
				'fs' : fs
			})
		return pools

#TODO: Change do dict!
def zpool_state_to_str(state):
	if state.name == "POOL_STATE_ACTIVE":
		return "active"
	elif state.name == "POOL_STATE_EXPORTED":
		return "exported"
	elif state.name == "POOL_STATE_DESTROYED":
		return "destroyed"
	elif state.name == "POOL_STATE_SPARE":
		return "spare"
	elif state.name == "POOL_STATE_L2CACHE":
		return "l2cache"
	elif state.name == "POOL_STATE_UNINITIALIZED":
		return "uninitialized"
	elif state.name == "POOL_STATE_UNAVAIL":
		return "unavailable"
	elif state.name == "POOL_STATE_POTENTIALLY_ACTIVE":
		return "potentially-active"
	else:
		return "unimplemented"

#TODO: Change do dict!
def zpool_status_to_str(status):
	if status.name == "ZPOOL_STATUS_CORRUPT_CACHE":
		return "Cache Corrupt"
	elif status.name == "ZPOOL_STATUS_MISSING_DEV_R":
		return "Device Missing"
	elif status.name == "ZPOOL_STATUS_MISSING_DEV_NR":
		return "Device Missing"
	elif status.name == "ZPOOL_STATUS_CORRUPT_LABEL_R":
		return "Corrupt Label"
	elif status.name == "ZPOOL_STATUS_CORRUPT_LABEL_NR":
		return "Corrupt Label"
	elif status.name == "ZPOOL_STATUS_BAD_GUID_SUM":
		return "Bad GUID Checksum"
	elif status.name == "ZPOOL_STATUS_CORRUPT_POOL":
		return "Corrupt Pool"
	elif status.name == "ZPOOL_STATUS_CORRUPT_DATA":
		return "Corrupt Data"
	elif status.name == "ZPOOL_STATUS_FAILING_DEV":
		return "Failed Device"
	elif status.name == "ZPOOL_STATUS_VERSION_NEWER":
		return "Newer ZPool Version"
	elif status.name == "ZPOOL_STATUS_HOSTID_MISMATCH":
		return "HostID Mismatch"
	elif status.name == "ZPOOL_STATUS_IO_FAILURE_WAIT":
		return "Failure, Waiting"
	elif status.name == "ZPOOL_STATUS_IO_FAILURE_CONTINUE":
		return "Failure, Continuing."
	elif status.name == "ZPOOL_STATUS_BAD_LOG":
		return "Bad Log Device"
	elif status.name == "ZPOOL_STATUS_ERRATA":
		return "Errata"
	elif status.name == "ZPOOL_STATUS_UNSUP_FEAT_READ":
		return "Unsupported Read Feature"
	elif status.name == "ZPOOL_STATUS_UNSUP_FEAT_WRITE":
		return "Unsupported Write Feature"
	elif status.name == "ZPOOL_STATUS_FAULTED_DEV_R":
		return "Faulted Device"
	elif status.name == "ZPOOL_STATUS_FAULTED_DEV_NR":
		return "Faulted Device"
	elif status.name == "ZPOOL_STATUS_VERSION_OLDER":
		return "Older Version"
	elif status.name == "ZPOOL_STATUS_FEAT_DISABLED":
		return "Disabled Feature"
	elif status.name == "ZPOOL_STATUS_RESILVERING":
		return "Resilvering"
	elif status.name == "ZPOOL_STATUS_OFFLINE_DEV":
		return "Offline Device"
	elif status.name == "ZPOOL_STATUS_REMOVED_DEV":
		return "Removed Device"
	elif status.name == "ZPOOL_STATUS_OK":
		return "Ok"
	else:
		return "Not Implemented."
