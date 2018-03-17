import json
import csv
import time
import threading
import requests
import random
from datetime import datetime

SERVER_URL = "http://localhost:5000/api/v1/data/customer/"
LAT_MIN = 34.04515933151722
LAT_MAX = 34.268398018498345
LONG_MIN = -117.95187009742699
LONG_MAX = -118.26353680421454

def post_customer_data(curr_location, destination, user_id):
  body = {
      "customer_id" : user_id,
      "current_location" : curr_location,
      "destination_location": destination,
      "arrival_time" : str(datetime.utcnow()),
      "estimated_time_stayed" : 0,
      'budget':0
  }
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.post(SERVER_URL, headers=header, json=body)
  #print response

class User(threading.Thread):
  def __init__(self, random_coordinates, my_id):
    self.random_coordinates = random_coordinates
    self.my_id = my_id
    threading.Thread.__init__(self)

  def run(self):
    while True:
      if len(self.random_coordinates) > 1:
        curr_loc = self.random_coordinates.pop()
        dest_loc = self.random_coordinates.pop()
        post_customer_data(curr_loc, dest_loc, self.my_id)
        time.sleep(3)


if __name__ == "__main__":
  random_coordinates = []
  # Specify an area for the user to make requests from
  for i in range(18):
    sensor = User(random_coordinates, i)
    sensor.start()
  while True:
    new_lat = random.uniform(LAT_MIN, LAT_MAX)
    new_long = random.uniform(LONG_MIN, LONG_MAX)
    new_loc = {'type': 'Point', 'coordinates': [new_long, new_lat]}
    random_coordinates.append(new_loc)
    if len(random_coordinates) > 1000:
      time.sleep(5)
