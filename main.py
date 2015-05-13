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
from models.smart import SmartInfo

api.add_resource(Pool, '/api/pools')
api.add_resource(Disk, '/api/disks')
api.add_resource(SmartInfo, '/api/smart/<string:disk>')

#TODO: Stats

# Start the application
if __name__ == '__main__':
	with LibZFSHandle():
		app.run(host="192.168.1.3",
    			port=5000)
