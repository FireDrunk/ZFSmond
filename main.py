#!/usr/bin/python

# Imports
from flask import Flask, send_from_directory
from flask.ext import restful
from libzfs.handle import LibZFSHandle

#Define Flask Application
app = Flask(__name__,static_url_path="/static")
app.debug = True

# MAIN Application Route (Serves AngularJS Main)
@app.route('/')
def root():
	return send_from_directory('static', 'index.html');

# Define the API Basics
api = restful.Api(app)

# Models
from models.disk import Disk
from models.zfs import Pool
from models.zfs import Filesystem
from models.smart import SmartInfo
from models.stats import Stats
from models.update import Update

# URL Definitions
api.add_resource(Pool, '/api/pools')
api.add_resource(Disk, '/api/disks')
api.add_resource(Filesystem, '/api/filesystems')
api.add_resource(SmartInfo, '/api/smart/<string:disk>')
api.add_resource(Stats, '/api/stats')
api.add_resource(Update, '/api/update')

# Start the application
if __name__ == '__main__':
		with LibZFSHandle():
			app.run(host="0.0.0.0",port=5000)
