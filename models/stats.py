from flask.ext import restful
from pySMART import Device
from libzfs.zpool import ZPool
from libzfs import bindings

## From the ZFSonLinux Git repo:
#
# hrtime_t	vs_timestamp;		/* time since vdev load	*/
# uint64_t	vs_state;		/* vdev state		*/
# uint64_t	vs_aux;			/* see vdev_aux_t	*/
# uint64_t	vs_alloc;		/* space allocated	*/
# uint64_t	vs_space;		/* total capacity	*/
# uint64_t	vs_dspace;		/* deflated capacity	*/
# uint64_t	vs_rsize;		/* replaceable dev size */
# uint64_t	vs_esize;		/* expandable dev size */
# uint64_t	vs_ops[ZIO_TYPES];	/* operation count	*/
# uint64_t	vs_bytes[ZIO_TYPES];	/* bytes read/written	*/
# uint64_t	vs_read_errors;		/* read errors		*/
# uint64_t	vs_write_errors;	/* write errors		*/
# uint64_t	vs_checksum_errors;	/* checksum errors	*/
# uint64_t	vs_self_healed;		/* self-healed bytes	*/
# uint64_t	vs_scan_removing;	/* removing?	*/
# uint64_t	vs_scan_processed;	/* scan processed bytes	*/
# uint64_t	vs_fragmentation;	/* device fragmentation */


class Stats(restful.Resource):
    def get(self):

        zio_type_t = bindings['zio_type_t']

        stats = []
        for pool in ZPool.list():
            pool.refresh_stats()

            stat = {}
            stat['pool_name'] = pool.name
            raw_stats = pool.config.vdev_tree.get('vdev_stats',None)
            if raw_stats:
                (timestamp, state, aux, alloc, space, dspace, rsize, esize) = raw_stats[:8]
                zio_ops = raw_stats[8:14]
                zio_bytes = raw_stats[14:20]
                fragmentation = None

                if len(raw_stats) > 26:
                    (read_errors, write_errors, checksum_errors, self_healed, scan_removing, scan_processed, fragmentation) = raw_stats[20:27]
                else:
                    (read_errors, write_errors, checksum_errors, self_healed, scan_removing, scan_processed) = raw_stats[20:26]
                stat['timestamp'] = timestamp
                stat['state'] = state
                stat['aux'] = aux
                stat['alloc'] = alloc
                stat['space'] = space
                stat['dspace'] = dspace
                stat['rsize'] = rsize
                stat['esize'] = esize

                stat['zio_ops'] = {key.name: int(zio_ops[key]) for key in zio_type_t if key < zio_type_t.ZIO_TYPES}

                stat['zio_bytes'] = {key.name: int(zio_bytes[key]) for key in zio_type_t if key < zio_type_t.ZIO_TYPES}

                stat['read_errors'] = read_errors
                stat['write_errors'] = write_errors
                stat['checksum_errors'] = checksum_errors
                stat['self_healed'] = self_healed
                stat['scan_removing'] = scan_removing
                stat['scan_processed'] = scan_processed

                stat['fragmentation'] = fragmentation

                stats.append(stat)
        return stats

        # return [
        #             {
        #                 'pool_name': 'archive',
        #                 'read_ops' : '10',
        #                 'write_ops' : '10',
        #                 'read_bandwith' : '100',
        #                 'write_bandwith' : '100',
        #             },
        #             {
        #                 'pool_name': 'test',
        #                 'read_ops' : '10',
        #                 'write_ops' : '10',
        #                 'read_bandwith' : '100',
        #                 'write_bandwith' : '100',
        #             }
        # ]
