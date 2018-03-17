import json
import csv
import time
import threading
import requests
from os import listdir
from os.path import isfile, join

SERVER_URL = "http://localhost:5000/api/v1/data/lot/"

# TODO: Find a good place to put this
lot_to_id = {
    u'Beach House Lot': 0,
    u'Structure 1': 1,
    u'Structure 2': 2,
    u'Structure 3': 3,
    u'Structure 4': 4,
    u'Structure 5': 5,
    u'Structure 6': 6,
    u'Structure 9': 7,
    u'Lot 8 North': 8,
    u'Lot 3 North': 9,
    u'Lot 1 North': 10,
    u'Pier Deck': 11,
    u'Lot 4 South': 12,
    u'Lot 5 South': 13,
    u'Civic Center': 14,
    u'Library': 15,
    u'Structure 7': 16,
    u'Structure 8': 17
}

# Reverse index for lot_to_id
id_to_lot = {lot_id: lot_name for (lot_name, lot_id) in lot_to_id.items()}

def post_lot_data(lot_id, available_spots, time):
  body = {"lot_id" : lot_id, "available_spots" : available_spots, "time": time}
  header = {"Accept" : "application/json", 
      "Content-Type": "application/json"}
  response = requests.post(SERVER_URL, headers=header, json=body)

class Sensor(threading.Thread):
  def __init__(self, my_id, data_file_path):
    self.my_id = my_id
    self.file_reader = csv.reader(open(data_file_path, 'r'))
    threading.Thread.__init__(self)

  def run(self):
    for row in self.file_reader:
      # Post data every 3 seconds
      post_lot_data(self.my_id, row[7], row[0])
      time.sleep(3)

if __name__ == "__main__":
  data_path = 'data/'
  data_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
  for i in range(len(data_files)):
    sensor = Sensor(i, data_path + data_files[i])
    sensor.start()
