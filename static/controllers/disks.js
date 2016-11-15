angular.module('zfsmond.disks',[])
	.controller('DisksController',['$scope','$http','$interval',function($scope, $http, $interval) {
		$scope.disks = [];
		$scope.smartinfo = [];

		var disks_updater = function() {
			$http.get('api/disks').
				success(function(data, status, headers, config)
				{
					$scope.disks = data
				}).
				error(function(data, status, headers, config)
				{
					console.log('Could not fetch updates!')
				});
		};
		var disks_interval = $interval(disks_updater, 1000);
		disks_updater();

		$scope.$on('$destroy', function() {
			$interval.cancel(disks_interval);
		});

		var http = $http;
		$scope.getSmart = function(dev) {
			http.get('api/smart/' + dev).success(function(smart_response){
				$scope.smartinfo[dev] = smart_response;
				console.log("SMART Info: " + smart_response);
			}).
			error(function(data, status, headers, config) {
				$scope.smartinfo[dev].error = true;
			});
		};

	}]);
