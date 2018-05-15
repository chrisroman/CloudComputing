import json
from . import *
import os
import requests
import pickle
import random

# Helper function to get the correct path
def make_path(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(dir_path, filename)

# Static information about all the sensors
lot_info_map = pickle.load(open(make_path("lot_info_map.p"), "rb"))


class GetUserReservationsController(AppDevController):

  def get_path(self):
    return '/reservations/user/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    # Randomly pick a lot id (and thus an area) to service this request.
    # The particular area doesn't matter because all the reservations are
    # stored in Dynamo, so any server can handle this
    lot_id = random.choice(lot_info_map.keys())

    # Forward the request to the appropriate area
    req_url = "http://{}/api/v1/reservations/user/{}".format(
        os.environ["EDGE_ALB_DNS"],
        lot_info_map[lot_id]["TopicID"],
    )

    resp = requests.get(req_url, headers=request.headers, data=request.data)

    print "Response: {}".format(resp.text)

    if resp.status_code == 200:
      return resp.json()["data"]
    else:
      return resp.text

