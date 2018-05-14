import os
import datetime
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mongoengine import MongoEngine
import config
from threading import Lock
from datetime import datetime


# Configure Flask app
app = Flask(__name__, static_url_path='/templates')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'location_history',
    'host': os.environ['MONGO_ADDRESS'],
    'port': 27017,
    'username': os.environ['MONGO_INITDB_ROOT_USERNAME'],
    'password': os.environ['MONGO_INITDB_ROOT_PASSWORD']
}

# Database
mysql_db = SQLAlchemy(app)
db = MongoEngine(app)
my_lot_ids = {}
my_lot_ids_lock = Lock()

parking_info = {}
parking_info_lock = Lock()

#All 17 lot ids can be mapped to min datetime, will be updated immediately

most_recent_timestamp = {}
most_recent_timestamp_lock = Lock()

file_lock = Lock()

model = []
model_lock = Lock()

# Check to make sure this is the main Flask app, not the debugger
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  # SQS Polling Thread starts running here
  from app.pcasts.models.edge_server import SQSPoller
  from app.pcasts.models.s3_poller import S3Poller
  sqs_poller = SQSPoller(parking_info, parking_info_lock, most_recent_timestamp, most_recent_timestamp_lock,
        my_lot_ids, my_lot_ids_lock)
  s3_poller = S3Poller(file_lock, model, model_lock)


# Import + Register Blueprints
from app.pcasts import pcasts as pcasts
app.register_blueprint(pcasts)
