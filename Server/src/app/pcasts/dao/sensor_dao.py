from . import *
#from . import pcasts
from app.pcasts import pcasts as pcasts

def add_sensor_data(lot_id, available_spots):
  pcasts.lot_info[lot_id] = available_spots
  #print (lot_id, available_spots)
