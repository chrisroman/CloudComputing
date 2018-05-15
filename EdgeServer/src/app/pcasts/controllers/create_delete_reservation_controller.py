import json
from . import *
import sys
import os

SERVER_ID = os.environ["SERVER_ID"]

class CreateDeleteReservationController(AppDevController):

  def get_path(self):
    return '/reservations/' + SERVER_ID

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
      return {'message': "Successfully inserted reservation"}
    if request.method == 'DELETE':
      reservations_dao.delete_reservation(user_id, \
          lot_id, start_time, end_time)
      return {'message': "Successfully deleted reservation"}
