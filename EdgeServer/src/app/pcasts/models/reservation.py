from sqlalchemy.orm import validates
from . import *

class Reservation(db.Model):
  __tablename__ = 'reservations'

  reservation_id = db.Column(db.Integer, primary_key=True)
  lot_id = db.Column(db.Integer)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.Integer, nullable=False)

  def __init__(self, **kwargs):
    self.lot_id = kwargs.get('lot_id')
    self.start_time = kwargs.get('start_time')
    self.end_time = kwargs.get('end_time')

  def __eq__(self, other_user):
    return self.id == other_user.id
