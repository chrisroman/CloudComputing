import datetime
import time
import requests
import json
import grequests
import pprint

EDGE_ALB_DNS = "edgealb-1163938868.us-east-1.elb.amazonaws.com"

def make_request():
  area_ids = [1, 2]
  URLS = [
      "http://{}/api/v1/prediction/{}".format( \
          EDGE_ALB_DNS, \
          area_id, \
      ) \
      for area_id in area_ids \
  ]
  print "Making requests to areas: {}".format(area_ids)
  rs = (grequests.get(u) for u in URLS)
  responses = grequests.map(rs)
  print "Responses: {}".format(responses)

  predictions = {}
  for resp in responses:
    if resp is not None and resp.status_code == 200:
      for (lot_id, prediction_info) in resp.json()["data"]["message"].items():
        predictions[lot_id] = prediction_info

  return predictions

response = make_request()
pprint.pprint(response)
