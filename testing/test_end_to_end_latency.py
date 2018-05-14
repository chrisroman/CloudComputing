import json
import random
import requests
import time

def test_create_reservation(data, num_requests):
  start_time = int(time.time())
  for i in range(num_requests):
    SERVER_URL = 'localhost:5000'
    RESERVATION_URL = "http://{}/api/v1/reservations/".format(SERVER_URL)
    info = data[i]
    body = {"lot_id" : info['lot_id'],
            "start_time": info['start_time']),
            "end_time": info['end_time']),
            "user_id": info['user_id'],}
    header = {"Accept" : "application/json",
              "Content-Type": "application/json"}
    response = requests.post(RESERVATION_URL, headers=header, data=json.dumps(body))
    return response
  end_time = int(time.time())
  duration = end_time - start_time
  avg_time = duration/num_requests
  print "Create reservation: Sending {} took a total of {} seconds and {} requests on average".join(num_requests, duration, avg_time)

def test_delete_reservation(data, num_requests):
  start_time = int(time.time())
  for i in range(num_requests):
    SERVER_URL = 'localhost:5000'
    RESERVATION_URL = "http://{}/api/v1/reservations/".format(SERVER_URL)
    info = data[i]
    body = {"lot_id" : info['lot_id'],
            "start_time": info['start_time']),
            "end_time": info['end_time']),
            "user_id": info['user_id'],}
    header = {"Accept" : "application/json",
              "Content-Type": "application/json"}
    response = requests.delete(RESERVATION_URL, headers=header, data=json.dumps(body))
    return response
  end_time = int(time.time())
  duration = end_time - start_time
  avg_time = duration/num_requests
  print "Delete reservation: Sending {} took a total of {} seconds and {} requests on average".join(num_requests, duration, avg_time)

if __name__ == '__main__':
  data = []
  num_requests = 10

  #Creating fake data
  for i in range(num_requests)
    temp_dict = {}
    temp_dict['user_id'] = random.randrange(0, 100000)
    temp_dict['lot_id'] = random.randrange(0, 100000)
    temp_dict['start_time'] = random.randrange(0, 100000)
    temp_dict['end_time'] = random.randrange(temp_dict['start_time'], 100000)
    data.append(temp_dict)

  test_create_reservation(data)
  test_delete_reservation(data)
