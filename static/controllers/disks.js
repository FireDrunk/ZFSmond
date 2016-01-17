angular.module('zfsmond.disks',[])
	.controller('DisksController',['$scope','$http', function($scope, $http) {
		$scope.disks = [];
		$scope.smartinfo = [];
		//$scope.http = $http;

		$http.get('/api/disks').
			success(function(data, status, headers, config)
			{
				$scope.disks = data;
			}).
			error(function(data, status, headers, config) {
				console.log('Error retreiving disk information from API!');
			});
		var http = $http;
		
		$scope.getSmart = function(dev) {
			console.log("Smart button pressed! (" + dev +")");
			http.get('/api/smart/' + dev).success(function(smart_response){
				$scope.smartinfo[dev] = smart_response;
				console.log("SMART Info: " + smart_response);
			}).
			error(function(data, status, headers, config) {
				$scope.smartinfo[dev].error = true;
			});
		};

	}]);
