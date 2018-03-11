import json
import csv
import time
import threading
import requests

SERVER_URL = "http://localhost:5000/api/v1/data/lot/"
LOT_DATA_PATH = 'data/ParkingLotCounts.csv'



def post_lot_data(lot_id, available_spots, time):
  body = {"lot_id" : lot_id, "available_spots" : available_spots, "time": time}
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.post(SERVER_URL, headers=header, json=body)
  #print response

class Sensor(threading.Thread):
  def __init__(self, messages, my_id):
    self.message_queue = messages
    self.my_id = my_id
    threading.Thread.__init__(self)


  def run(self):
    while True:
      if len(self.message_queue) > 0:
        row = self.message_queue.pop()
        
        post_lot_data(1, row[7], row[0])
        time.sleep(3)

if __name__ == "__main__":
  messages = []
  myFile = open(LOT_DATA_PATH, 'r')
  reader = csv.reader(myFile)
  for i in range(18):
    sensor = Sensor(messages, i)
    sensor.start()
  for row in reader:
    messages.append(row)
    if len(messages) > 1000:
      time.sleep(5)
