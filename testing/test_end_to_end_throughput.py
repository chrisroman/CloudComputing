import json
import time
import threading
import requests
import random
import multiprocessing
from multiprocessing import Pool

NUM_AREAS = 3
MAX_USERS = 10
MAX_LOT_ID = 15
PERCENT_GET_USER_RESERVATIONS = 5
PERCENT_MAKE_RESERVATION = 15
PERCENT_DELETE_RESERVATION = 30
PERCENT_GET_PARKING_LOTS = 50
REQUEST_URL = "webalb-157542678.us-east-1.elb.amazonaws.com"
REQUEST_BASE = "http://{}/api/v1".format(REQUEST_URL)
LAT_MIN = 34.04515933151722
LAT_MAX = 34.268398018498345
LONG_MIN = -117.95187009742699
LONG_MAX = -118.26353680421454
NUM_REQUESTS = 500
CACHE_NUM_REQUESTS = 250
HEADER = {"Accept" : "application/json",
          "Content-Type": "application/json"}
Reservations = []

def verify_responses(responses):
  for response in responses:
    r = json.loads(response[2])
    assert r['success']

def test_load_multiprocess(action_id=-1, num_requests=0):
  Reservations = []
  data = []

  #First create num_requests of random data
  for i in range(num_requests):
    if action_id == -2: #both delete and get parking
      rand_num = random.randint(16, 49)
    if action_id == -1:
      rand_num = random.randint(0, 99)
    else:
      rand_num = action_id
    action = get_random_request(rand_num)
    data.append(action)

  #Spawn pool
  p = multiprocessing.Pool(11)
  start_time = time.time() * 1000
  responses = p.map(execute_requests, data)
  end_time = time.time() *1000
  total_time = end_time - start_time
  verify_responses(responses)
  return total_time

def execute_requests(data):
  if data['action'] == "get_user_rev":
    RESERVATION_URL = REQUEST_BASE + "/reservations/user/"
    body = {
      "user_id" : data['user_id']
    }
    response = requests.get(RESERVATION_URL, headers=HEADER, data=json.dumps(body))
  elif data['action'] == "create_reserve":
    RESERVATION_URL = REQUEST_BASE + "/reservations/"
    body = {
      "user_id" : data['user_id'],
      "lot_id" : data['lot_id'],
      "start_time" : data['start_time'],
      "end_time" : data['end_time'],
    }
    response = requests.post(RESERVATION_URL, headers=HEADER, data=json.dumps(body))
  elif data['action'] == "delete_reserve":
    RESERVATION_URL = REQUEST_BASE + "/reservations/"
    body = {
      "user_id" : data['user_id'],
      "lot_id" : data['lot_id'],
      "start_time" : data['start_time'],
      "end_time" : data['end_time'],
    }
    response = requests.delete(RESERVATION_URL, headers=HEADER, data=json.dumps(body))
  elif data['action'] == "get_lots":
    RESERVATION_URL = REQUEST_BASE + "/prediction/?dest_lat={}&dest_lon={}&time={}&lot_range={}"\
        .format(data['dest_lat'], data['dest_lon'], data['time'], data['lot_range'])
    body = {}
    response = requests.get(RESERVATION_URL, headers=HEADER)
  else:
    raise Error('Unknown Action')
  return (RESERVATION_URL,body,response.text)

def get_random_request(i):
  request = {}
  if i < 5: #get reservations for user
    request['action'] = "get_user_rev"
    request['user_id'] = random.randint(0, MAX_USERS-1)
    return request
  if i < 20: # delete reservations
    if len(Reservations) > 1:
      request_index = random.randrange(len(Reservations)-1)
      request = Reservations[request_index]
      del Reservations[request_index]
      request['action'] = "delete_reserve"
      return request
  if i < 50: # create reservations
    request['action'] = "create_reserve"
    request['user_id'] = random.randint(0, MAX_USERS-1)
    request['lot_id'] = random.randrange(0, MAX_LOT_ID)
    request['start_time'] = random.randrange(0, 100000)
    request['end_time'] = random.randrange(0, 100000)
    request['reservation_id'] = "{};{};{}".format(request['user_id'],request['lot_id'],request['start_time'])
    Reservations.append(request)
    return request
  if i < 100: # get parking lots
    request['action'] = "get_lots"
    request['dest_lat'] = random.uniform(LAT_MIN, LAT_MAX)
    request['dest_lon'] = random.uniform(LONG_MIN, LONG_MAX)
    request['time'] = random.randint(0,15)
    request['lot_range'] = random.randint(0,5)
    return request

def heat_cache():
  total_time = test_load_multiprocess(action_id=-1, num_requests=CACHE_NUM_REQUESTS)
  print "Total time in seconds to make {} requests to heat chache: {}"\
      .format(CACHE_NUM_REQUESTS,total_time)

def test_parking_endpoint(num_requests):
  total_time = test_load_multiprocess(action_id=75, num_requests=num_requests)
  print "Total time in seconds to make {} requests for parking spots endpoint: {}"\
      .format(num_requests,total_time)

def test_reservation_endpoint(num_requests):
  total_time = test_load_multiprocess(action_id=-2, num_requests=num_requests)
  print "Total time in ms to make {} requests for create/delete reservation endpoint : {}"\
      .format(num_requests,total_time)

def test_get_user_reservation_endpoint(num_requests):
  total_time = test_load_multiprocess(action_id=2, num_requests=num_requests)
  print "Total time in ms to make {} requests for get user reservation endpoint : {}"\
      .format(num_requests,total_time)

def test_joint_endpoint(num_requests):
  total_time = test_load_multiprocess(action_id=-1, num_requests=num_requests)
  print "Total time in ms to make {} requests for a random mix of all endpoint : {}"\
      .format(num_requests,total_time)

if __name__ == '__main__':
  print "Heating up server cache by sending {} random requests and let server start polling".format(CACHE_NUM_REQUESTS)
  heat_cache()
  time.sleep(5)
  print "Testing scenario 1: {} parking requests".format(NUM_REQUESTS)
  test_parking_endpoint(NUM_REQUESTS)
  print "Clearing up server cache by sending {} random requests and let server start polling".format(CACHE_NUM_REQUESTS)
  heat_cache()
  time.sleep(5)
  print "Testing scenario 2: {} reservation requests".format(NUM_REQUESTS)
  test_reservation_endpoint(NUM_REQUESTS)
  print "Clearing up server cache by sending {} random requests and let server start polling".format(CACHE_NUM_REQUESTS)
  heat_cache()
  time.sleep(5)
  print "Testing scenario 3: {} get all reservations for a user".format(NUM_REQUESTS)
  test_get_user_reservation_endpoint(NUM_REQUESTS)
  time.sleep(5)
  print "Testing scenario 4: {} random interleaved reservation and parking requests".format(2*NUM_REQUESTS)
  test_joint_endpoint(NUM_REQUESTS)
