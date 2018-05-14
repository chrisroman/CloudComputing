import json
from . import *
from app import parking_info, parking_info_lock, most_recent_timestamp, 
    most_recent_timestamp_lock, my_lot_ids, my_lot_ids_lock, model, model_lock
import os
import sys
from datetime import datetime


#SERVER_ID = os.environ["SERVER_ID"]
SERVER_ID = '0'

class SensorPredictionController(AppDevController):

  def get_path(self):
    # Query parameters:
    # - lot_id: The id of the lot that information is being requested from
    return '/prediction/' + SERVER_ID

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    print "Executing code from path /lot/"
    print "Information being requested from lot {}".format(lot_id)

    #Return all the data a user could want - return a dictionary of values
    request_data = {}
    
    for lot_id in my_lot_ids:
      with most_recent_timestamp_lock:
        timestamp = most_recent_timestamp[lot_id]
      with parking_info_lock:
        available_spots = parking_info[lot_id][timestamp]

      num_intervals_15_min_ago = timestamp - datetime.timedelta(minutes=15)
      num_intervals_30_min_ago = timestamp - datetime.timedelta(minutes=30)
      num_intervals_45_min_ago = timestamp - datetime.timedelta(minutes=30)
      num_intervals_60_min_ago = timestamp - datetime.timedelta(minutes=60)
      num_intervals_120_min_ago = timestamp - datetime.timedelta(minutes=120)
      num_intervals_180_min_ago = timestamp - datetime.timedelta(minutes=180)

      previous_timestamps = [num_intervals_15_min_ago, num_intervals_30_min_ago, num_intervals_45_min_ago
          num_intervals_60_min_ago, num_intervals_120_min_ago, num_intervals_180_min_ago]

      previous_available_spots = [0]*len(previous_timestamps)

      sufficient_data = True

      with parking_info_lock:
        for i in range (len(previous_available_spots)):
          if (previous_timestamps[i] in parking_info[lot_id]):
            previous_available_spots[i] = parking_info[lot_id][previous_timestamps[i]]
          else:
            sufficient_data = False

      if (not sufficient_data):
        continue

      predicted_available_spots = 0
      with model_lock:
        for i in range (len(previous_available_spots)):
          predicted_available_spots += (model[i] * previous_available_spots[i])

      request_data[(lot_id, timestamp)] = predicted_available_spots


    # Print out predictions
    print "Predictions for 15 min in the future: {}".format(request_data)

    # Flush stdout
    sys.stdout.flush()
    return {'message': request_data}
    

