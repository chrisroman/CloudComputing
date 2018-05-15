import boto3
import time

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Reservations')

print(table.creation_date_time)

response = table.query(
    KeyConditionExpression=Key('Parking ').eq(1) & Key('')
    )
item = response['Item']
print(item)

table.put_item(
    Item={
      'Parking ': 1,
      'Expiration': 1000,
      }
    )

user_lot_id = {'user_id': 5, 'lot_id': 6}
table.put_item(Item={'area_id': 2, 'user_lot_id': json.dumps(user_lot_id), 'user_id': user_lot_id['user_id'], 'lot_id': user_lot_id['lot_id'], 'end_time': 100})

