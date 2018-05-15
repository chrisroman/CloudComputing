import json
from . import *
import pickle
from math import sin, cos, sqrt, atan2, radians
import requests
import os

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
    dest_lat = float(request.args.get('dest_lat'))
    dest_lon = float(request.args.get('dest_lon'))

    # Find the closest lot
    distances = {
        lot_id: calc_dist(dest_lat, dest_lon, info["Latitude"], info["Longitude"])
        for (lot_id, info) in lot_info_map.items()
    }
    closest_lot_id = min(distances, key=distances.get)

    # Get the relevant parking lot information based on the cluster that is
    # responsible for the closest parking lot's information
    # TODO: Extend this to possibly contact multiple edge servers for more
    # parking lot information
    req_url = "http://{}/api/v1/prediction/{}" \
        .format(
            os.environ["EDGE_ALB_DNS"],
            lot_info_map[closest_lot_id]["TopicID"],
        )
    print "Closest Lot: {} - {}".format(closest_lot_id, lot_info_map[closest_lot_id])
    print "Getting parking lot information from URL: {}".format(req_url)
    resp = requests.get(req_url)
    print "Response: {}".format(resp.text)


    if resp.status_code == 200:
      return resp.json()["data"]
    else:
      return resp.text

