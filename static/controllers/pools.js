angular.module('zfsmond.pools',[])
	.controller('PoolsController', ['$scope','$http','$interval',function($scope, $http, $interval) {
		$scope.pools = []

		function startsWith(string, prefix) {
			return string.slice(0, prefix.length) == prefix;
		}

		var pools_updater = function() {
			$http.get('api/pools').
				success(function(data, status, headers, config) 
				{
					$scope.pools = data;
					angular.forEach($scope.pools, function(pool) {
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
					});
				}).
				error(function(data, status, headers, config) {
					console.log('Could not fetch updates!')
				});
		}
		var pools_interval = $interval(pools_updater, 1000);
		pools_updater();

		$scope.$on('$destroy', function() {
			$interval.cancel(pools_interval);
		});
	}]);
