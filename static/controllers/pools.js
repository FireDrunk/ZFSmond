angular.module('zfsmond.pools',[])
	.controller('PoolsController', function($http) {
		var poolCtrl = this
		this.pools = []

		$http.get('/api/pools').
			success(function(data, status, headers, config) 
			{
				poolCtrl.pools = data;
			}).
			error(function(data, status, headers, config) {
				console.log('Error!')
			});

	});
