angular.module('zfsmond.pools',[])
	.controller('PoolsController', function($http) {
		var poolCtrl = this
		this.pools = []

		function startsWith(string, prefix) {
			return string.slice(0, prefix.length) == prefix;
		}

		$http.get('/api/pools').
			success(function(data, status, headers, config) 
			{
				poolCtrl.pools = data;
				angular.forEach(poolCtrl.pools, function(pool) {
					if (startsWith(pool.status, "Cache") ||
							startsWith(pool.status, "Device") ||
							startsWith(pool.status, "Corrupt") ||
							startsWith(pool.status, "Bad") ||
							startsWith(pool.status, "Failed") ||
							startsWith(pool.status, "HostID") ||
							pool.status == "Failure, Waiting" ||
							startsWith(pool.status, "Unsupported") ||
							startsWith(pool.status, "Faulted") ||
							startsWith(pool.status, "Offline") ||
							startsWith(pool.status, "Removed")) {
						pool.status_color = "error";
					} else if (pool.status == "HostID Mismatch" ||
							pool.status == "Failure, Continuing" ||
							pool.status == "Newer ZPool version" ||
							pool.status == "Older version" ||
							pool.status == "Resilvering") {
						pool.status_color = "warning";
					} else if (pool.status == "Errata" ||
						pool.status == "Disabled feature") {
						pool.status_color = "info";
					} else {
						pool.status_color = "ok";
					}
					console.log(pool.status_color);
				});
			}).
			error(function(data, status, headers, config) {
				console.log('Error!')
			});

	});
