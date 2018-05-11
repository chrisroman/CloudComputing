import json
from . import *

class CreateDeleteReservationController(AppDevController):

  def get_path(self):
    return '/reservations/'

  def get_methods(self):
    return ['POST', 'DELETE']

  def content(self, **kwargs):
    body = json.loads(request.data)
    if request.method == 'POST':
      lot_id = body['lot_id']
      start_time = body['start_time']
      end_time = body['end_time']
      reservations_dao.create_reservation(lot_id, start_time, end_time)
    if request.method == 'DELETE':
      reservation_id = body['reservation_id']
      reservations_dao.delete_reservation(reservation_id)
    return {}
