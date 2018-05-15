import json
from . import *
import pickle
from math import sin, cos, sqrt, atan2, radians
import requests
import os
import grequests
import sys

# approximate radius of earth in km
R = 6373.0

# Helper function to get the correct path
def make_path(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(dir_path, filename)

# Static information about all the sensors
lot_info_map = pickle.load(open(make_path("lot_info_map.p"), "rb"))

# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def calc_dist(st_lat, st_lon, end_lat, end_lon):
  lat1 = radians(st_lat)
  lon1 = radians(st_lon)
  lat2 = radians(end_lat)
  lon2 = radians(end_lon)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  distance = R * c

  return distance

class LotRangeQueryController(AppDevController):

  def get_path(self):
    """
      Query String:
        - curr_lat:
        - curr_lon:
        - dest_lat:
        - dest_lon:
        - departTime:
        - arrivalTime:
    """
    return '/prediction/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    print "********************   TESTING   ******************************"
    dest_lat = float(request.args.get('dest_lat'))
    dest_lon = float(request.args.get('dest_lon'))
    time = float(request.args.get('time'))
    lot_range = float(request.args.get('lot_range')) # IN KM

    # Find the closest lot
    distances = {
        lot_id: calc_dist(dest_lat, dest_lon, info["Latitude"], info["Longitude"])
        for (lot_id, info) in lot_info_map.items()
    }
    print "Distances: {}".format(distances)
    sys.stdout.flush()


    # Get the relevant parking lot information based on the cluster that is
    # responsible for the closest parking lot's information
    in_range_ids = [lot_id for (lot_id, dist) in distances.items() \
        if dist <= lot_range]
    area_ids = set([lot_info_map[lot_id]["TopicID"] for lot_id in in_range_ids])

    URLS = [
        "http://{}/api/v1/prediction/{}".format( \
            os.environ["EDGE_ALB_DNS"], \
            area_id, \
        ) \
        for area_id in area_ids \
    ]
    print "Making requests to areas: {}".format(area_ids)
    sys.stdout.flush()
    rs = (grequests.get(u) for u in URLS)
    responses = grequests.map(rs)
    print "Responses: {}".format(responses)
    sys.stdout.flush()

    predictions = {}
    for resp in responses:
      print resp
      sys.stdout.flush()
      if resp is not None and resp.status_code == 200:
        print resp.json()
        sys.stdout.flush()
        for (lot_id, prediction_info) in resp.json()["data"]["message"].items():
          if distances[lot_id] <= lot_range:
            predictions[lot_id] = prediction_info

    return predictions
