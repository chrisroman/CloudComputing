import boto3
import time
import os
import pickle

# Get AWS resources for later use
sns_client = boto3.client('sns')
sqs_client = boto3.client('sqs')
sns = boto3.resource('sns')
sqs = boto3.resource('sqs')

# Helper function to get the correct path
def make_path(filename):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(dir_path, filename)


SENSOR_ID = int(os.environ['SENSOR_ID'])

# Note SNS Topic Arns have the format arn:aws:sns:region:account-id:topicname
list_topics_resp = sns_client.list_topics()

# Sort the arns, which should sort such that id 0 maps to the 0th topic,
# id 1 maps to the 1st topic, etc. This way, we can use the environment
# variable for this sensor's id in order to figure out which topic it should
# publish to
topic_arns = sorted([topic["TopicArn"] for topic in list_topics_resp["Topics"]])

print "Received topic arns: {}".format(topic_arns)

lotid_to_topics = pickle.load(open(make_path("lotid_to_topics.p"), "rb"))
topic_id = lotid_to_topics[SENSOR_ID]
publishing_topic_arn = topic_arns[topic_id]

print "====== Starting to publish to topic {} ======".format(publishing_topic_arn)
msg_id = 0
while True:
  sns_client.publish(
      TopicArn = publishing_topic_arn,
      Message = "Msg {}".format(msg_id)
  )
  print "Publishing message 'Msg {}'".format(msg_id)
  msg_id += 1
  time.sleep(3)
