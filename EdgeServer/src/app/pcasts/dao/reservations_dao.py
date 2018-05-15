import os
from . import *
from app import parking_info, most_recent_timestamp
from app.pcasts.models.reservation import *


def create_reservation(user_id, lot_id, start_time, end_time):
  # Check that lot_id actually exists for this server. There is no
  # public api so this will always be correct
  if True:
    reservation_count = get_reservation_count(lot_id, start_time, end_time)
    current_count = reservation_count[most_recent_timestamp[int(lot_id)]]
    max_count = 5
    if reservation_count == max_count:
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
      return response
    else:
      raise Exception("All parking spots are already reserved during this time")
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
  response = client.query(
      TableName='Reservations',
      IndexName='lot_id-end_time-index',
      KeyConditionExpression='lot_id = :lid AND end_time <= :end',
      FilterExpression='start_time >= :s',
      ExpressionAttributeValues = {
        ':s': {'N': '{}'.join(start_time)},
        ':lid': {'N': '{}'.join(lot_id)},
        ':end': {'N': '{}'.join(end_time)},
      },
      ConsistentRead=False
  )
  return response['Count']


def get_strong_reservation_count(lot_id, start_time, end_time):
  response = client.query(
      TableName='Reservations',
      IndexName='area_id-lot_id-index',
      KeyConditionExpression='area_id = :area AND lot_id = lid',
      FilterExpression='start_time >= :s AND end_time <= :end',
      ExpressionAttributeValues = {
        ':area': {'N': '{}'.join(os.environ['SERVER_ID'])},
        ':s': {'N': '{}'.join(start_time)},
        ':lid': {'N': '{}'.join(lot_id)},
        ':end': {'N': '{}'.join(end_time)},
      },
      ConsistentRead=True
  )
  return response['Count']

def get_reservations_by_user_id(user_id):
  response = client.query(
      TableName='Reservations',
      IndexName='user_id-index',
      KeyConditionExpression='user_id = :uid',
      ExpressionAttributeValues = {
        ':uid': {'N': '{}'.format(user_id)},
      },
  )
  print response
  return response['Count']
