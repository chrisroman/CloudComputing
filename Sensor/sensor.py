import boto3
import time
import os
import sys
import pickle
import csv
import json

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

ID_PADDING = 4
lot_filename = "data/lot{}.csv".format(str(SENSOR_ID).zfill(ID_PADDING))
lot_path = make_path(lot_filename)

# Ensure file exists. If not, just exit
if not os.path.isfile(lot_path):
  print "Couldn't find file with path {}. Exiting...".format(lot_path)
  sys.exit(1)

print "====== Starting to publish to topic {} ======".format(publishing_topic_arn)
with open(lot_path, 'rb') as csvfile:
  csv_reader = csv.reader(csvfile, delimiter=',')

  # SKIP THE FIRST LINE WITH THE COLUMN NAMES
  csv_reader.next()

  # The (0-indexed) column number in the csv file that contains the 
  # number of available parking spots, and timestamp
  AVAILABLE_SPOTS_COLUMN = 7
  TIMESTAMP_COLUMN = 0

  # Publish sensor data from csv file
  for row in csv_reader:
    msg_dict = {
      "lot_id": SENSOR_ID,
      "available_spots": row[AVAILABLE_SPOTS_COLUMN],
      "timestamp": row[TIMESTAMP_COLUMN]
    }
    sns_client.publish(
        TopicArn = publishing_topic_arn,
        Message = json.dumps(msg_dict)
    )
    print "Publishing message '{}'".format(json.dumps(msg_dict))
    time.sleep(3)
