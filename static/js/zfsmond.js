var app = angular.module('zfsmond', ['ui.bootstrap', 'ui.router','ngResource', 'zfsmond.pools','zfsmond.filesystems', 'zfsmond.disks', 'zfsmond.stats']);

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
		if (bytes == 0) return 0;
		if (isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '-';
		if (typeof precision === 'undefined') precision = 1;
		var units = ['bytes', 'kiB', 'MiB', 'GiB', 'TiB', 'PiB'],
			number = Math.floor(Math.log(bytes) / Math.log(1024));
		return (bytes / Math.pow(1024, Math.floor(number))).toFixed(precision) +  ' ' + units[number];
	}
});

app.filter('bytes_1000', function() {
	return function(bytes, precision) {
		if (bytes == 0) return 0;
		if (isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '-';
		if (typeof precision === 'undefined') precision = 1;
		var units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'],
			number = Math.floor(Math.log(bytes) / Math.log(1024));
		return (bytes / Math.pow(1000, Math.floor(number))).toFixed(precision) +  ' ' + units[number];
	}
});

app.filter('scrub_state_to_text', function() {
	return function(state){
		switch(state) {
			case 2: return "Finished";
			case 1: return "Running";
			default: return "Unknown"
		}
	}
});

app.filter('scrub_state_to_class', function() {
	return function(state) {
			switch (state) {
				case 2: return "success";
				case 1: return "warning";
				default: return "default";
			}
	}
});

app.filter('time_to_text', function() {
	return function(time) {
    var minutes = time / 60;
    secs = Math.floor(time % 60);
    var hours = minutes / 60;
    minutes = Math.floor(minutes % 60);
    hours = Math.floor(hours % 24);
		if (hours < 10)
			var real_hours = "0" + hours;
		else
			var real_hours = hours;
		if (minutes < 10)
			var real_minutes = "0" + minutes;
		else
				var real_minutes = minutes;
		if (secs < 10)
			var real_secs = "0" + secs
		else
			var real_secs = secs;
    return real_hours + ":" + real_minutes + ":" + real_secs;
	}
});
