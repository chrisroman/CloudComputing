from . import *
from app import db
import datetime

class CustomerInfo(db.Document):
    customer_id             = db.IntField(required=True)
    current_location        = db.PointField(required=True)
    destination_location    = db.PointField(required=True)
    arrival_time            = db.DateTimeField(required=True)
    estimated_time_stayed   = db.IntField(required=True)        # Minutes
    budget                  = db.FloatField(required=True)      # Dollars
