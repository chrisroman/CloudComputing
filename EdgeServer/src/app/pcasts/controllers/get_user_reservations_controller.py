import json
from . import *

class GetUserReservationController(AppDevController):

  def get_path(self):
    return '/reservations/user/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    body = json.loads(request.data)
    user_id = body['user_id']
    reservations = reservations_dao.get_reservations_by_user_id(user_id)
    return {'reservations' : reservations}
