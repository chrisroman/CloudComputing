import boto3
import pickle
sns_client = boto3.client('sns')
sqs_client = boto3.client('sqs')
sns = boto3.resource('sns')
sqs = boto3.resource('sqs')


BASE_TOPIC_NAME = "area"

lot_info_map = pickle.load(open("lot_info_map.p", "rb"))
NUM_TOPICS = len(set( [info["TopicID"] for info in lot_info_map.values()] ))

# Used to give ids leading zeros, e.g. 0 -> 0003
ID_PADDING = 4

# Create Topics and Queues
topic_arns = []
for topic_id in range(NUM_TOPICS):
  print "=========== Starting Iteration {} ===========".format(topic_id)
  topic_name = BASE_TOPIC_NAME + str(topic_id).zfill(ID_PADDING)

  print "Creating/getting topic {}".format(topic_name)
  topic_resp = sns_client.create_topic(
      Name = topic_name
  )
  print "Done creating/getting topic {}\n".format(topic_name)
  topic_arn = topic_resp["TopicArn"]
  topic_arns.append(topic_arn)

  print "=========== End Iteration {} ===========\n".format(topic_id)


