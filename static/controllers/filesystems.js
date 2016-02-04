angular.module('zfsmond.filesystems',[])
	.controller('FilesystemsController', ['$scope','$http','$interval',function($scope, $http, $interval) {
		$scope.pools = []

		var filesystems_updater = function() {
			$http.get('/api/filesystems').
				success(function(data, status, headers, config)
				{
					$scope.pools = data
				}).
				error(function(data, status, headers, config)
				{
					console.log('Could not fetch updates!')
				});
		};
		var filesystems_interval = $interval(filesystems_updater, 1000);
		filesystems_updater();

		$scope.$on('$destroy', function() {
			$interval.cancel(filesystems_interval);
		});
	}]);

