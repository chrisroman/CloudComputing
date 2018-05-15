import os
from . import *
from app import parking_info, most_recent_timestamp
from app.pcasts.models.reservation import *

AREA_ID = int(os.environ['SERVER_ID'])

def create_reservation(user_id, lot_id, start_time, end_time):
  # Check that lot_id actually exists for this server. There is no
  # public api so this will always be correct
  if True:
    reservation_count = get_weak_reservation_count(lot_id, start_time, end_time)
    # current_count = reservation_count[most_recent_timestamp[int(lot_id)]]
    max_count = 5
    if reservation_count < max_count:
      response = reservations.put_item(
         Item={
              'area_id' : int(os.environ['SERVER_ID']),
              'reservation_id': "{};{};{}".format(user_id, lot_id, start_time),
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

def delete_reservation(user_id, lot_id, start_time):
  response = reservations.delete_item(
      Key={
          "area_id": AREA_ID,
          "reservation_id": "{};{};{}".format(user_id, lot_id, start_time)
      }
  )
  print response

def get_weak_reservation_count(lot_id, start_time, end_time):
  response = client.query(
      TableName='Reservations',
      IndexName='lot_id-end_time-index',
      KeyConditionExpression='lot_id = :lid AND end_time <= :end',
      FilterExpression='start_time >= :s',
      ExpressionAttributeValues = {
        ':s': {'N': '{}'.format(start_time)},
        ':lid': {'N': '{}'.format(lot_id)},
        ':end': {'N': '{}'.format(end_time)},
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
        ':area': {'N': '{}'.format(AREA_ID)},
        ':s': {'N': '{}'.format(start_time)},
        ':lid': {'N': '{}'.format(lot_id)},
        ':end': {'N': '{}'.format(end_time)},
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
