from . import *
#from . import pcasts
#from app.pcasts import pcasts as pcasts

# def add_customer(customer_id, current_location,
#         destination_location, arrival_time, estimated_time_stayed, budget):
#   pcasts.customer_info[customer_id] = {}
#   pcasts.customer_info[customer_id]['current_location'] = current_location
#   pcasts.customer_info[customer_id]['destination_location'] = destination_location
#   pcasts.customer_info[customer_id]['arrival_time'] = arrival_time
#   pcasts.customer_info[customer_id]['estimated_time_stayed'] = estimated_time_stayed
#   pcasts.customer_info[customer_id]['budget'] = budget

from app.pcasts.models.customer_info import *

# In-Memory Store
customer_info = {}

def add_customer(customer_id, current_location,
        destination_location, arrival_time, estimated_time_stayed, budget):
  customer_info[customer_id] = {}
  customer_info[customer_id]['current_location'] = current_location
  customer_info[customer_id]['destination_location'] = destination_location
  customer_info[customer_id]['arrival_time'] = arrival_time
  customer_info[customer_id]['estimated_time_stayed'] = estimated_time_stayed
  customer_info[customer_id]['budget'] = budget
  print {'message': 'Added customer {} going from {} to {}' \
        .format(customer_id, current_location, destination_location)}
  info = CustomerInfo(customer_id = customer_id,
  		current_location = current_location,
        destination_location = destination_location,
        arrival_time = arrival_time,
        estimated_time_stayed = estimated_time_stayed,
        budget = budget)
  info.save()
  print CustomerInfo.objects().count()



  #print (lot_id, available_spots)