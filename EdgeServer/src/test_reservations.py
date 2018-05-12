import datetime
import requests
import json

SERVER_URL = 'edgealb-1163938868.us-east-1.elb.amazonaws.com'
RESERVATION_URL = "http://{}/api/v1/reservations/".format(SERVER_URL)

def make_request():
  body = {"lot_id" : 0,
          "start_time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
          "end_time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
          "reservation_id": 0}
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.post(RESERVATION_URL, headers=header, data=json.dumps(body))
  return response

response = make_request()
print response.content
data = json.loads(response.content)
print data
