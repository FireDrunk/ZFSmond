angular.module('zfsmond.smart',[])
	.controller('SmartController', ['$scope','$http',function($scope, $http) {

		$http.get('api/smart').
			success(function(data, status, headers, config)
			{
        for(i=0; i < data.length; i++)
        {
          $scope.disks[i].smart = data;
        }
			}).
			error(function(data, status, headers, config) {
				console.log('Error!')
			});
	}]);
