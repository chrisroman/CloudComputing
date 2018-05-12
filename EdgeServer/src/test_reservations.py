import datetime
import requests
import json

SERVER_URL = ''
RESERVATION_URL = "http://{}/api/v1/reservations/".format(SERVER_URL)

def make_request():
  body = {"lot_id" : 1,
          "start_time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
          "end_time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
          "reservation_id" : 1}
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.delete(RESERVATION_URL, headers=header, data=json.dumps(body))
  return response

response = make_request()
print response.content
data = json.loads(response.content)
print data
