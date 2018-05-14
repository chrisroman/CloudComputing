import os
from . import *
from app.pcasts.models.reservation import *


def create_reservation(user_id, lot_id, start_time, end_time):
  # Check that lot_id actually exists for this server. There is no
  # public api so this will always be correct
  if True:
    reservation_count = get_reservation_count(lot_id, start_time, end_time)
    response = reservations.put_item(
       Item={
            'area_id' : int(os.environ['SERVER_ID']),
            'user_lot_id' : str(user_id) + str(lot_id),
            'lot_id': lot_id,
            'start_time': start_time,
            'end_time': end_time,
            'user_id' : user_id,
        }
    )
    print response
  else:
    raise Exception("Invalid lot_id provided")

def delete_reservation(user_id, lot_id, start_time, end_time):
  response = reservations.put_item(
     Item={
          'area_id' : int(os.environ['SERVER_ID']),
          'user_lot_id' : str(user_id) + str(lot_id),
          'lot_id': lot_id,
          'start_time': start_time,
          'end_time': end_time,
          'user_id' : user_id,
      }
  )
  print respones

def get_weak_reservation_count(lot_id, start_time, end_time):
  response = client.scan(
      TableName='Reservations',
      IndexName='lot_id-end_time-index',
      FilterExpression='end_time < :end AND start_time >= :start',
      ExpressionAttributeValues = {
        ':end': {'N': '30'},
        ':start': {'N': '0'},
      },
      ConsistentRead=False
  )
  print response

def get_strong_reservation_count(lot_id, start_time, end_time):
  response = client.scan(
      TableName='Reservations',
      IndexName='area_id-lot_id-index',
      FilterExpression='end_time < :end AND start_time >= :start',
      ExpressionAttributeValues = {
        ':end': {'N': '30'},
        ':start': {'N': '0'},
      },
      ConsistentRead=True
  )
  json
