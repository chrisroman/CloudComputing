import datetime
import time
import requests
import json

SERVER_URL = 'localhost:5000'
RESERVATION_URL = "http://{}/api/v1/reservations/".format(SERVER_URL)

def make_request():
  body = {"lot_id" : 0,
          "start_time": int(time.time()),
          "end_time": int(time.time()),
          "user_id": 100, }
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.post(RESERVATION_URL, headers=header, data=json.dumps(body))
  return response

response = make_request()
print response.content
data = json.loads(response.content)
print data
