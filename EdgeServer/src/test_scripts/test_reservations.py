import datetime
import time
import requests
import json

SERVER_URL = 'webalb-157542678.us-east-1.elb.amazonaws.com'
RESERVATION_URL = "http://{}/api/v1/reservations/".format(SERVER_URL)

def make_request(user_id):
  body = {"lot_id" : 1,
          "start_time": int(time.time()),
          "end_time": int(time.time()) + 3600, # int(time.time())
          "user_id": user_id, }
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.post(RESERVATION_URL, headers=header, data=json.dumps(body))
  return response

user_id = raw_input("Make an insertion for which user_id? ")
response = make_request(int(user_id))
print response.content
data = json.loads(response.content)
print data
