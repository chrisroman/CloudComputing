import json
from . import *

class CreateDeleteReservationController(AppDevController):

  def get_path(self):
    return '/reservations/'

  def get_methods(self):
    return ['POST', 'DELETE']

  def content(self, **kwargs):
    body = json.loads(request.data)
    user_id = body['user_id']
    lot_id = body['lot_id']
    start_time = body['start_time']
    end_time = body['end_time']
    if request.method == 'POST':
      reservations_dao.create_reservation(user_id, \
          lot_id, start_time, end_time)
    if request.method == 'DELETE':
      reservations_dao.delete_reservation(user_id, \
          lot_id, start_time, end_time)
    return {}
