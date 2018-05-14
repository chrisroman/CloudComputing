from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.pcasts.models.reservation import *

class ReservationSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Reservation
