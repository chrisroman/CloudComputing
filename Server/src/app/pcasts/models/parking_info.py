from . import *
from app import db
import datetime

class ParkingInfo(db.Document):
    lot_id = db.IntField(required=True)
    available_spots = db.IntField(required=True)
    time = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
