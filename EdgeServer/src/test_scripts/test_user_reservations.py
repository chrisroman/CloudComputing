import datetime
import time
import requests
import json
import pprint

SERVER_URL = 'webalb-157542678.us-east-1.elb.amazonaws.com'
RESERVATION_URL = "http://{}/api/v1/reservations/user/".format(SERVER_URL)

def make_request(user_id):
  body = {"user_id": user_id}
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.get(RESERVATION_URL, headers=header, data=json.dumps(body))
  return response

user_id = raw_input("Find reservations for which user_id? ")
response = make_request(int(user_id))
data = json.loads(response.content)
pprint.pprint(data)
