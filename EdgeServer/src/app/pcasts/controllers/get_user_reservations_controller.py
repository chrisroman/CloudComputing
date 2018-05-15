import json
from . import *
import sys
import os

SERVER_ID = os.environ["SERVER_ID"]

class GetUserReservationController(AppDevController):

  def get_path(self):
    return '/reservations/user/' + SERVER_ID

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    body = json.loads(request.data)
    user_id = body['user_id']
    count = reservations_dao.get_reservations_by_user_id(user_id)
    return {'reservations' : count}
