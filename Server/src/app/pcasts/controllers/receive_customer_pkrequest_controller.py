import json
from . import *

class ReceiveCustomerParkingRequestController(AppDevController):

  def get_path(self):
    return '/data/customer/'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    body = json.loads(request.data)
    customer_id = body['customer_id']
    current_location = body['current_location']
    destination_location = body['destination_location']
    arrival_time =  body['arrival_time']
    '''
    The following two will be default values if user opts not to provide tje information 
    and can be handled accordingly
    '''
    estimated_time_stayed = body['estimated_time_stayed']
    budget = body['budget']
    customers_dao.add_customer(customer_id, current_location,
        destination_location, arrival_time, estimated_time_stayed, budget)
    print {'message': 'Added customer {} going from {} to {}' \
        .format(customer_id, current_location, destination_location)} 
    return {'message': 'Added customer {} going from {} to {}' \
        .format(customer_id, current_location, destination_location)} 
