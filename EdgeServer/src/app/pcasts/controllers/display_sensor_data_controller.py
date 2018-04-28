import json
from . import *
from app import parking_info, parking_info_lock

class DisplaySensorDataController(AppDevController):

  def get_path(self):
    # Query parameters:
    # - lot_id: The id of the lot that information is being requested from
    return '/lot/'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    print "Executing code from path /lot/"
    lot_id = request.args.get('lot_id')
    print "Information being requested from lot {}".format(lot_id)

    # Display lot information in the queue
    with parking_info_lock:
      print "parking_info: {}".format(parking_info)

    return {'message': parking_info}
