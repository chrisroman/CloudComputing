import datetime
import time
import requests
import json

SERVER_URL = 'webalb-157542678.us-east-1.elb.amazonaws.com'
RESERVATION_URL = "http://{}/api/v1/reservations/user/".format(SERVER_URL)

def make_request():
  body = {"user_id": 420}
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.get(RESERVATION_URL, headers=header, data=json.dumps(body))
  return response

response = make_request()
print response.content
data = json.loads(response.content)
print data
