from . import *
from app.pcasts.models.reservation import *


def create_reservation(lot_id, start_time, end_time):
  if True: #Check that lot_id actually exists for this server
    resrevation = Reservation(lot_id=lot_id, start_time=start_time, \
        end_time=end_time)
    return mysql_db_utils.commit_model(resrevation)
  else:
    raise Exception("Invalid lot_id provided")

def delete_reservation(reservation_id):
  maybe_reservation = Reservation.query.filter(Reservation.reservation_id == \
      reservation_id).first()
  if maybe_reservation is not None:
    return mysql_db_utils.delete_model(maybe_reservation)
  raise Exception('Specified reservation does not exist')
