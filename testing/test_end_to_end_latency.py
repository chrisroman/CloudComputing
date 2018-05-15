import json
import random
import requests
import time
import test_end_to_end_throughput

### Run emulate throughput before you start these tests to get a
### realistic measure of how average server load affects the latency

NUM_LATENCY_REQUESTS = 10

def test_joint_endpoint_latency():
  data = create_data(-1)
  test_name = "test_joint_endpoint_latency"
  make_requests(test_name, data)

def test_reservation_endpoint_latency():
  data = create_data(-2)
  test_name = "test_reservation_endpoint_latency"
  make_requests(test_name, data)

def test_get_user_reservation_endpoint_latency():
  data = create_data(2)
  test_name = "test_get_user_reservation_endpoint_latency"
  make_requests(test_name, data)

def test_get_lot_info_reservation():
  data = create_data(-1)
  test_name = "test_get_lot_info_reservation"
  make_requests(test_name, data)


def create_data(action_id):
  data = []
  action_id = -1
  #First create num_requests of random data
  for i in range(NUM_LATENCY_REQUESTS):
    if action_id == -2: #both delete and get parking
      rand_num = random.randint(16, 49)
    if action_id == -1:
      rand_num = random.randint(0, 99)
    else:
      rand_num = action_id
    action = test_end_to_end_throughput.get_random_request(rand_num)
    data.append(action)
  return data

def make_requests(test_name, data):
  requests_to_validate = []
  print "Testing {}: for latency".format(test_name)
  start_time = time.time() * 1000
  for i in range(NUM_LATENCY_REQUESTS):
    dat = test_end_to_end_throughput.execute_requests(data[i])
    requests_to_validate.append(dat)
  end_time = time.time() *1000
  total_time = end_time - start_time
  test_end_to_end_throughput.verify_responses(requests_to_validate)
  print "All responses were successful"
  print "10 sequential requests took {} ms for a total of {} ms latency per request"\
      .format(total_time, total_time/NUM_LATENCY_REQUESTS)

if __name__ == '__main__':
  print "Hi"
  test_get_lot_info_reservation()
  test_reservation_endpoint_latency()
  test_get_user_reservation_endpoint_latency()
  test_joint_endpoint_latency()
