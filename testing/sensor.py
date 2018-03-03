import json
import csv
import time
import requests

SERVER_URL = "http://localhost:5000/api/v1/data/"
LOT_ID = 764978

def post_lot_data(lot_id, availble_spots, time):
  body = {"lot_id" : lot_id, "availble_spots" : availble_spots, "time": time}
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.post(SERVER_URL, headers=header, json=body)

if __name__ == "__main__":
  myFile = open('data/Lot1Data.csv', 'r')
  reader = csv.reader(myFile)
  for row in reader:
    post_lot_data(LOT_ID, row[7], row[0])
    time.sleep(2)
