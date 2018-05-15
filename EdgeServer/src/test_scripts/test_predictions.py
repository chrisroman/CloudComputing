import datetime
import time
import requests
import json
import grequests
import pprint

EDGE_ALB_DNS = "edgealb-1163938868.us-east-1.elb.amazonaws.com"
WEB_ALB_DNS = "webalb-157542678.us-east-1.elb.amazonaws.com"
URL1 = "http://{}/api/v1/prediction/?dest_lat=34.02516&dest_lon=-118.50977&time=1.0&lot_range=1.25".format(WEB_ALB_DNS)
URL2 = "http://{}/api/v1/prediction/?dest_lat=34.00226&dest_lon=-118.48608&time=1.0&lot_range=1.25".format(WEB_ALB_DNS)

def make_request(url):
  body = {"lot_id" : 0,
          "start_time": 420,
          "end_time": 420, # int(time.time())
          "user_id": 420, }
  header = {"Accept" : "application/json",
            "Content-Type": "application/json"}
  response = requests.get(url, headers=header, data=json.dumps(body))
  return response

query_id = raw_input("Which query to perform? 1 or 2? ")
if int(query_id) == 1:
  response = make_request(URL1)
elif int(query_id) == 2:
  response = make_request(URL2)

pprint.pprint(json.loads(response.content))
