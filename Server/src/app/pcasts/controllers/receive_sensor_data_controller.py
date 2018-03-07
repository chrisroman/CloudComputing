import json
from . import *

class ReceiveSensorDataController(AppDevController):

  def get_path(self):
    return '/data/lot/'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    body = json.loads(request.data)
    time = body['time']
    open_spots = body['available_spots']
    lot_id = body['lot_id']
    sensor_dao.add_sensor_data(lot_id, open_spots)
    return {'message': 'Added lot {} with {} available spots' \
        .format(lot_id, open_spots)}
