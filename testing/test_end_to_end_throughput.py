import json
import time
import threading
import requests
import random
from multiprocessing import Pool

##XXX: Pools to avoid possible GIL effect on IO operations
NUM_AREAS = 3
MAX_USERS = 10
PERCENT_GET_USER_RESERVATIONS = 5
PERCENT_MAKE_RESERVATION = 15
PERCENT_DELETE_RESERVATION = 30
PERCENT_GET_PARKING_LOTS = 50
REQUEST_URL = "localhost"
REQUEST_BASE = "http://{}/api/v1".format(REQUEST_URL)
LAT_MIN = 34.04515933151722
LAT_MAX = 34.268398018498345
LONG_MIN = -117.95187009742699
LONG_MAX = -118.26353680421454
NUM_REQUESTS = 200
HEADER = {"Accept" : "application/json",
          "Content-Type": "application/json"}
Reservations = []

def heat_cache(num_requests):
  data = []
  #First create num_requests of random data
  for i in range(num_requests):
    action = get_random_request()
    data.append(action)
  #Spawn pool
  p = multiprocessing.Pool(6)
  start_time = int(time.time())
  p.map(execute_requests, data)
  end_time = int(time.time())
  total_time = end_time - start_time
  print "Total time in seconds to make {} requests to heat chache: {}".format(num_requests,total_time)

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
      "area_id" : data['area_id'],
      "start_time" : data['start_time'],
      "end_time" : data['end_time'],
      "reservation_id" : data['reservation_id'],
    }
    response = requests.post(RESERVATION_URL, headers=HEADER, data=json.dumps(body))
  elif data['action'] == "delete_reserve":
    RESERVATION_URL = REQUEST_BASE + "/reservations/"
    body = {
      "user_id" : data['user_id'],
      "lot_id" : data['lot_id'],
      "area_id" : data['area_id'],
      "start_time" : data['start_time'],
      "end_time" : data['end_time'],
      "reservation_id" : data['reservation_id'],
    }
    response = requests.delete(RESERVATION_URL, headers=HEADER, data=json.dumps(body))
  elif data['action'] == "get_lots":

  else:
    raise Error('Unknown Action')

def get_random_request():
  randint = random.randint(0, 99)
  request = {}
  if i < 5: #get reservations for user
    request['action'] = "get_user_rev"
    request['user_id'] = random.randint(0, MAX_USERS-1)
    return request
  elif i < 20: # delete reservations
    request_index = random.randint(0, len(Reservations)-1)
    request = request[request_index]
    del request[request_index]
    request['action'] = "delete_reserve"
    return request
  elif i < 50: # create reservations
    request['action'] = "create_reserve"
    request['user_id'] = random.randint(0, MAX_USERS-1)
    request['lot_id'] = random.randrange(0, 100000)
    request['start_time'] = random.randrange(0, 100000)
    Reservations.append(request)
    return request
  elif i < 99: # get parking lots
    request['action'] = "get_lots"
    request['']
    return request

if __name__ == '__main__':
  print "Heating up server cache by sending {} random requests and let server start polling".join(NUM_REQUESTS)
  heat_cache(NUM_REQUESTS)
  exit(0)
  print "Testing scenario 1: {} parking requests".join(NUM_REQUESTS)
  test_parking_endpoint(NUM_REQUESTS)
  print "Clearing up server cache by sending {} random requests and let server start polling".join(NUM_REQUESTS)
  heat_cache(NUM_REQUESTS)
  print "Testing scenario 2: {} reservation requests".join(NUM_REQUESTS)
  test_reservation_endpoint(NUM_REQUESTS)
  print "Clearing up server cache by sending {} random requests and let server start polling".join(NUM_REQUESTS)
  heat_cache(NUM_REQUESTS)
  print "Testing scenario 3: {} random interleaved reservation and parking requests".join(2*NUM_REQUESTS)
  test_joint_endpoint(NUM_REQUESTS)

    #
    # new_lat = random.uniform(LAT_MIN, LAT_MAX)
    # new_long = random.uniform(LONG_MIN, LONG_MAX)
    # new_loc = {'type': 'Point', 'coordinates': [new_long, new_lat]}
    # random_coordinates.append(new_loc)
    # if len(random_coordinates) > 1000:
    #   time.sleep(5)
