from flask import Blueprint
from app import *

# PCasts Blueprint
pcasts = Blueprint('pcasts', __name__, url_prefix='/api/v1')

# Import all models
from app.pcasts.models._all import *

# Import all controllers
from app.pcasts.controllers.hello_world_controller import *
from app.pcasts.controllers.receive_sensor_data_controller import *
from app.pcasts.controllers.receive_customer_pkrequest_controller import *


pcasts.lot_info = {}

pcasts.customer_info = {}

controllers = [
    HelloWorldController(),
    ReceiveSensorDataController(),
    ReceiveCustomerParkingRequestController(),
    LotRangeQueryController(),
]

# Setup all controllers
for controller in controllers:
  pcasts.add_url_rule(
      controller.get_path(),
      controller.get_name(),
      controller.response,
      methods=controller.get_methods()
  )
