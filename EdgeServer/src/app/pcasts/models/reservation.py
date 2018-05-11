from app import mysql_db
from sqlalchemy.orm import validates
from . import *

class Reservation(mysql_db.Model):
  __tablename__ = 'reservations'

  reservation_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
  lot_id = mysql_db.Column(mysql_db.Integer)
  start_time = mysql_db.Column(mysql_db.DateTime, nullable=False)
  end_time = mysql_db.Column(mysql_db.Integer, nullable=False)

  def __init__(self, **kwargs):
    self.lot_id = kwargs.get('lot_id')
    self.start_time = kwargs.get('start_time')
    self.end_time = kwargs.get('end_time')

  def __eq__(self, other_user):
    return self.id == other_user.id
