angular.module('zfsmond.stats',[])
	.controller('StatsController', ['$scope','$http',function($scope, $http)
  {
    var statsCtrl = this
		statsCtrl.stats = []

		$http.get('/api/stats').
			success(function(data, status, headers, config)
			{
        statsCtrl.stats = data
			}).
			error(function(data, status, headers, config) {
				console.log('Error!')
			});
	}]);
