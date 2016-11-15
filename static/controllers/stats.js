angular.module('zfsmond.stats',[])
	.controller('StatsController', ['$scope','$http','$interval',function($scope, $http, $interval) {
		$scope.stats = []

		var stats_updater = function() {
			$http.get('api/stats').
				success(function(data, status, headers, config)
				{
					$scope.stats = data
				}).
				error(function(data, status, headers, config) {
					console.log('Could not fetch updates!')
				});
		};
		var stats_interval = $interval(stats_updater, 1000);
		stats_updater();

		// listen on DOM destroy (removal) event, and cancel the next UI update
		// to prevent updating time after the DOM element was removed.
		$scope.$on('$destroy', function() {
			$interval.cancel(stats_interval);
		});
	}]);
