import os
import datetime
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
import config
from sqs_poller.edge_server import SQSPoller
from threading import Lock


# Configure Flask app
app = Flask(__name__, static_url_path='/templates')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'location_history',
    'host': '0.0.0.0',
    'port': 27017
}

parking_info = {}
parking_info_lock = Lock()

# Check to make sure this is the main Flask app, not the debugger
# if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  # SQS Polling Thread starts running here
  # poller = SQSPoller(parking_info, parking_info_lock)


# Database
# db = SQLAlchemy(app)
db = MongoEngine(app)

# Import + Register Blueprints
from app.pcasts import pcasts as pcasts
app.register_blueprint(pcasts)

# HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#   return render_template('404.html'), 404
