import json
from . import *
from app import parking_info, parking_info_lock, most_recent_timestamp, most_recent_timestamp_lock, my_lot_ids, my_lot_ids_lock
import os
import sys


SERVER_ID = os.environ["SERVER_ID"]

class DisplaySensorDataController(AppDevController):

  def get_path(self):
    # Query parameters:
    # - lot_id: The id of the lot that information is being requested from
    return '/area/' + SERVER_ID

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    #Return all the data a user could want - return a dictionary of values
    request_data = {}

    for my_lot_id in my_lot_ids:
      with most_recent_timestamp_lock:
        recent_timestamp = most_recent_timestamp[my_lot_id]
      with parking_info_lock:
        request_data[my_lot_id] = {
            "available_spots": parking_info[my_lot_id][recent_timestamp],
            "updated_at": recent_timestamp.strftime('%m/%d/%y %H:%M')
        }

    # Display lot information in the queue

    print "parking request info: {}".format(request_data)

    # Flush stdout
    sys.stdout.flush()
    return {'message': request_data}
