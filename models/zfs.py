from libzfs import *
from libzfs import zpool
from libzfs.zpool import zpool_prop_t
from libzfs import zdataset
from flask.ext import restful
import time

class Pool(restful.Resource):
	def get(self):
		pools = []
		for raw_pool in zpool.ZPool.list():
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
		config['guid'] = pool.config['pool_guid']
		config['scrub'] = self.get_scan_status(pool.config['vdev_tree']['children'][0].get('scan_stats', None))

		#config['raw'] = pool.config
		nr_of_vdevs = pool.config['vdev_children']
		config['nr_of_vdevs'] = nr_of_vdevs

		vdevs = []
		for vdev_config in pool.config['vdev_tree']['children']:
			# Skip weird vdev types
			if vdev_config['type'] == 'hole':
				continue

			# Test if the VDEV has children
			children = vdev_config.get('children', None)

			vdev_children = []
			if children:
				for child in vdev_config['children']:
					vdev_children.append({
							'type': child['type'],
							'path': child['path'],
							'name': ''.join(child['path'].split('/')[-1]),
					})
			else:
				vdev_children.append({
						'type': vdev_config['type'],
						'path': vdev_config['path'],
						'name': ''.join(vdev_config['path'].split('/')[-1]),
				})

			vdevs.append({
				'ashift' : vdev_config['ashift'],
				'nparity' : vdev_config.get('nparity', None),
				'type' : vdev_config['type'],
				'vdev_stats': vdev_config.get('vdev_stats', None),
				'children' : vdev_children
			})

		config['vdevs'] = vdevs

		return config
	def get_scan_status(self, stats):
	    if stats is None:
			return {"state" : "none requested"}
	    else:
			(func, state, start_time, end_time, to_examine, examined, to_process,processed, errors, pass_examined, pass_start) = stats
			return {
					'func' : func,
					'state' : state,
					'start_time' : start_time,
					'elapsed' : int(time.time()) - start_time,
					'end_time' : end_time,
					'to_examine' : to_examine,
					'examined' : examined,
					'to_process' : to_process,
					'processed' : processed,
					'errors' : errors,
					'pass_examined' : pass_examined,
					'pass_start' : pass_start
					}

class Filesystem(restful.Resource):
	def get(self):
		pools = []
		for pool in zpool.ZPool.list():
			fs = []
			for raw_fs in zdataset.ZDataset.list():
				fs_pool_name = raw_fs.name.split('/')[0]
				if fs_pool_name == pool.name:
					for sub_fs in raw_fs.child_filesystems():
						props = {key.name: value  for key, value in sub_fs.properties.items()}

						# Snapshots
						snaps = []
						for sub_snap in sub_fs.child_snapshots():
							snap_props = {key.name: value  for key, value in sub_snap.properties.items()}

							snaps.append(
								{
									'name' : ''.join(sub_snap.name.split('/')[1:]),
									'referenced' : snap_props['ZFS_PROP_REFERENCED'],
									'used' : snap_props['ZFS_PROP_LOGICALUSED'],
								})

						fs.append(
							{
								'name' : ''.join(sub_fs.name.split('/')[1:]),
								'available' : props['ZFS_PROP_AVAILABLE'],
								'referenced' : props['ZFS_PROP_REFERENCED'],
								'used' : props['ZFS_PROP_LOGICALUSED'],
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
