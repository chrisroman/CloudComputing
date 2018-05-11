import os
import datetime
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
import config
from threading import Lock


# Configure Flask app
app = Flask(__name__, static_url_path='/templates')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'location_history',
    'host': os.environ['MONGO_ADDRESS'],
    'port': 27017
}

# Database
mysql_db = SQLAlchemy(app)
db = MongoEngine(app)
parking_info = {}
parking_info_lock = Lock()
file_lock = Lock()

# Check to make sure this is the main Flask app, not the debugger
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  # SQS Polling Thread starts running here
  from app.pcasts.models.edge_server import SQSPoller
  from app.pcasts.models.s3_poller import S3Poller
  sqs_poller = SQSPoller(parking_info, parking_info_lock)
  # s3_poller = S3Poller(file_lock)


# Import + Register Blueprints
from app.pcasts import pcasts as pcasts
app.register_blueprint(pcasts)
