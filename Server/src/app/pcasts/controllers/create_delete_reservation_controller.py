import json
from . import *
import os
import requests

# Helper function to get the correct path
def make_path(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(dir_path, filename)

# Static information about all the sensors
lot_info_map = pickle.load(open(make_path("lot_info_map.p"), "rb"))


class CreateDeleteReservationController(AppDevController):

  def get_path(self):
    return '/reservations/'

  def get_methods(self):
    return ['POST', 'DELETE']

  def content(self, **kwargs):
    body = json.loads(request.data)
    lot_id = body['lot_id']

    # Forward the request to the appropriate area
    req_url = "http://{}/api/v1/reservations/{}".format(
        os.environ["EDGE_ALB_DNS"],
        lot_info_map[lot_id]["TopicID"],
    )

    if request.method == "POST":
      resp = requests.post(req_url, data=request.data)
    elif request.method == "DELETE":
      resp = requests.delete(req_url, headers=request.headers, data=request.data)

    print "Response: {}".format(resp.text)

    if resp.status_code == 200:
      return resp.json()["data"]
    else:
      return resp.text

