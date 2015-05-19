angular.module('zfsmond.stats',[])
	.controller('StatsController', ['$scope','$http','$interval',function($scope, $http, $interval)
  {
    var statsCtrl = this
		statsCtrl.stats = []

		var auto_update_stats = $interval(function () {
			$http.get('/api/stats').
				success(function(data, status, headers, config)
				{
	        statsCtrl.stats = data
				}).
				error(function(data, status, headers, config) {
					console.log('Error!')
				});
		}, 1000);

		// listen on DOM destroy (removal) event, and cancel the next UI update
		// to prevent updating time after the DOM element was removed.
		$scope.$on("$destroy", function() {
			$interval.cancel(auto_update_stats);
		});
	}]);
