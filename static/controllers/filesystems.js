angular.module('zfsmond.filesystems',[])
	.controller('FilesystemsController', function($http) {
		var fsCtrl = this
		this.pools = []

		$http.get('/api/filesystems').
			success(function(data, status, headers, config)
			{
				fsCtrl.pools = data;
			}).
			error(function(data, status, headers, config) {
				console.log('Error!')
			});

	});
