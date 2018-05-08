from . import *
#from . import pcasts
# from app.pcasts import pcasts as pcasts

# def add_sensor_data(lot_id, available_spots):
#   pcasts.lot_info[lot_id] = available_spots
  #print (lot_id, available_spots)

from app.pcasts.models.parking_info import *

def add_sensor_data(lot_id, availble_spots, time=None):
  info = ParkingInfo(lot_id=lot_id, available_spots=availble_spots) \
      if time is None \
      else ParkingInfo(lot_id=lot_id, available_spots=availble_spots, time=time)
  info.save()
