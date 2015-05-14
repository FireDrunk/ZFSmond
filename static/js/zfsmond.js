var app = angular.module('zfsmond', ['ui.bootstrap', 'ui.router','ngResource', 'zfsmond.pools','zfsmond.filesystems', 'zfsmond.disks']);

app.config(function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise("/pools")

	$stateProvider.state('pools', {
		url: "/pools",
		templateUrl: "/static/tabs/pools.html",
		controller: 'PoolsController as poolCtrl'
	});

	$stateProvider.state('filesystems', {
		url: "/filesystems",
		templateUrl: "/static/tabs/filesystems.html",
		controller: 'FilesystemsController as fsCtrl'
	});

	$stateProvider.state('disks', {
		url: "/disks",
		templateUrl: "/static/tabs/disks.html",
		controller: 'DisksController as diskCtrl'
	});

	$stateProvider.state('stats', {
		url: "/stats",
		templateUrl: "/static/tabs/stats.html",
		controller: 'StatsController as statsCtrl'
	});
});

app.filter('bytes', function() {
	return function(bytes, precision) {
		if (isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '-';
		if (typeof precision === 'undefined') precision = 1;
		var units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'],
			number = Math.floor(Math.log(bytes) / Math.log(1024));
		return (bytes / Math.pow(1024, Math.floor(number))).toFixed(precision) +  ' ' + units[number];
	}
});

app.filter('bytes_1000', function() {
	return function(bytes, precision) {
		if (isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '-';
		if (typeof precision === 'undefined') precision = 1;
		var units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'],
			number = Math.floor(Math.log(bytes) / Math.log(1024));
		return (bytes / Math.pow(1000, Math.floor(number))).toFixed(precision) +  ' ' + units[number];
	}
});
