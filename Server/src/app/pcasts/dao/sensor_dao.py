from . import *
from . import pcasts

def add_sensor_data(lot_id, availble_spots):
  pcasts.lot_info[lot_id] = availble_spots
