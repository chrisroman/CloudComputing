import json
from . import *
import pickle

# Helper function to get the correct path
def make_path(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(dir_path, filename)

sensor_info_map = pickle.load(open(make_path("sensor_info_map.p"), "rb"))

class LotRangeQueryController(AppDevController):

  def get_path(self):
    """
      Query String:
        - currLocLat:
        - currLocLong:
        - destLocLat:
        - destLocLong:
        - departTime:
        - arrivalTime:
    """
    return '/lots/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    body = json.loads(request.data)
    lot_id = request.args.get('lot_id')

    # customer_id = body['customer_id']

