from . import *
from app import db
import datetime

class CustomerInfo(db.Document):
    customer_id = db.IntField(required=True)
    current_location = db.StringField(max_length=200, required=True)
    destination_location = db.StringField(max_length=200, required=True)
    arrival_time = db.DateTimeField(required=True)
    #hours
    estimated_time_stayed = db.IntField(required=True)
    #dollars
    budget = db.IntField(required=True)

