import boto3
import json
import pprint

client = boto3.client('dynamodb')
# response = client.query(
#     TableName='Reservations',
#     IndexName='area_id-lot_id-index',
#     FilterExpression='end_time < :end AND start_time >= :start',
#     ExpressionAttributeValues = {
#       ':end': {'N': '30'},
#       ':start': {'N': '0'},
#     },
#     ConsistentRead=True
# )
# print response

response = client.query(
    TableName='Reservations',
    IndexName='lot_id-end_time-index',
    KeyConditionExpression='lot_id = :lid AND end_time <= :end',
   FilterExpression='start_time >= :s',
    ExpressionAttributeValues = {
     ':s': {'N': '-20'},
      ':lid': {'N': '5'},
      ':end': {'N': '15'},
    },
    ConsistentRead=False
)
count = response['Count']
print count
pprint.pprint(response)
