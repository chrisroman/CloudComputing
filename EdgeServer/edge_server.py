import boto3
import json
import os
import uuid

sns_client = boto3.client('sns')
sqs_client = boto3.client('sqs')
sns = boto3.resource('sns')
sqs = boto3.resource('sqs')


# Add policy to queue to allow sns to write to it
def allow_sns_to_write_to_sqs(topicarn, queuearn):
  policy_document = """{{
  "Version":"2012-10-17",
  "Statement":[
    {{
      "Sid":"MyPolicy",
      "Effect":"Allow",
      "Principal" : {{"AWS" : "*"}},
      "Action":"SQS:SendMessage",
      "Resource": "{}",
      "Condition":{{
        "ArnEquals":{{
          "aws:SourceArn": "{}"
        }}
      }}
    }}
  ]
}}""".format(queuearn, topicarn)
  return policy_document


################################################
#               Program start                  #
################################################

SERVER_ID = int(os.environ["SERVER_ID"])
BASE_QUEUE_NAME = "sensordata"
ID_PADDING = 4
server_uuid = uuid.uuid4()
queue_name = BASE_QUEUE_NAME + str(SERVER_ID).zfill(ID_PADDING) + "_" + str(server_uuid)

# Create a new queue
print "====== Begin queue creation and setup ======"
print "Creating/getting queue {}".format(queue_name)
queue_url = sqs_client.create_queue(
    QueueName = queue_name
)["QueueUrl"]
print "Finished creating/getting queue {}\n".format(queue_name)
queue = sqs.Queue(queue_url)

# Retrieve topic arn associated with this SERVER_ID
topic_arns = [topic["TopicArn"] for topic in sns_client.list_topics()["Topics"]]
topic_arns.sort()
topic_arn = topic_arns[SERVER_ID]

# Set required policies for the queue
policy_json = allow_sns_to_write_to_sqs(topic_arn, queue.attributes["QueueArn"])
response = sqs_client.set_queue_attributes(
    QueueUrl = queue_url,
    Attributes = {
        'MessageRetentionPeriod': '60',   # In seconds
        'Policy': policy_json,
        'VisibilityTimeout': '120', # In seconds
    }
)

# Subscribe the queue to the topic
print "Subscribing {} to topic {}".format(queue_name, topic_arn)
sub_response = sns_client.subscribe(
    TopicArn = topic_arn,
    Protocol = 'sqs',
    Endpoint = queue.attributes["QueueArn"]
)
print "Finished subscribing {} to topic {}".format(queue_name, topic_arn)
sub_arn = sub_response["SubscriptionArn"]
print "====== Finished queue creation and setup ======\n"


# Begin pulling messages from the queue
print "========= Starting to pull messages from {} =========".format(queue_url)
while True:
  # Start receiving messages
  messages = queue.receive_messages(
      AttributeNames=[
        'All'
      ],
      WaitTimeSeconds=10,
      MaxNumberOfMessages=10
  )
  # print(messages)
  if len(messages) == 0:
    print "No messages available..."
  else:
    print "Received {} messages".format(len(messages))

  for msg in messages:
    print json.loads(msg.body)["Message"]
    msg.delete()

