import boto3
import json
import os
import uuid
import threading
import time
from datetime import datetime
from datetime import timedelta
from app.pcasts.dao import sensor_dao
import random
import sys

class SQSPoller(object):
  """ Threading example class
  The run() method will be started and it will run in the background
  until the application exits.
  """

  def __init__(self, parking_info, parking_info_lock, most_recent_timestamp, most_recent_timestamp_lock,
        my_lot_ids, my_lot_ids_lock):
    """ Constructor
    :type parking_info: dict
    :param parking_info: Queue of messages of parking spot sensor data

    :type parking_info_lock: threading.Lock
    :param parking_info_lock: Lock for parking_info
    """

    self.sns_client = boto3.client('sns')
    self.sqs_client = boto3.client('sqs')
    self.sns = boto3.resource('sns')
    self.sqs = boto3.resource('sqs')
    self.parking_info = parking_info
    self.parking_info_lock = parking_info_lock
    self.most_recent_timestamp = most_recent_timestamp
    self.most_recent_timestamp_lock = most_recent_timestamp_lock
    self.my_lot_ids = my_lot_ids
    self.my_lot_ids_lock = my_lot_ids_lock

    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

  # Add policy to queue to allow sns to write to it
  def allow_sns_to_write_to_sqs(self, topicarn, queuearn):
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


  def run(self):
    """ Method that runs forever """
    ################################################
    #               Program start                  #
    ################################################

    print('Running Thread')
    #SERVER_ID = int(os.environ["SERVER_ID"])
    SERVER_ID = 0
    BASE_QUEUE_NAME = "sensordata"
    ID_PADDING = 4
    server_uuid = uuid.uuid4()
    queue_name = BASE_QUEUE_NAME + str(SERVER_ID).zfill(ID_PADDING) + "_" + str(server_uuid)

    # Create a new queue
    print "====== Begin queue creation and setup ======"
    print "Creating/getting queue {}".format(queue_name)
    queue_url = self.sqs_client.create_queue(
        QueueName = queue_name
    )["QueueUrl"]
    print "Finished creating/getting queue {}\n".format(queue_name)
    queue = self.sqs.Queue(queue_url)

    # Retrieve topic arn associated with this SERVER_ID
    topic_arns = [topic["TopicArn"] for topic in self.sns_client.list_topics()["Topics"]]
    topic_arns.sort()
    topic_arn = topic_arns[SERVER_ID]

    # Set required policies for the queue
    policy_json = self.allow_sns_to_write_to_sqs(topic_arn, queue.attributes["QueueArn"])
    response = self.sqs_client.set_queue_attributes(
        QueueUrl = queue_url,
        Attributes = {
            'MessageRetentionPeriod': '60',   # In seconds
            'Policy': policy_json,
            'VisibilityTimeout': '120', # In seconds
        }
    )

    # Subscribe the queue to the topic
    print "Subscribing {} to topic {}".format(queue_name, topic_arn)
    sub_response = self.sns_client.subscribe(
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

      for raw_msg in messages:
        decoded_msg = json.loads(raw_msg.body)

        # Messages are coming in as JSON dumps of dicts
        msg_contents = json.loads(decoded_msg["Message"])
        print msg_contents

        # Add message to the shared queue for consumers
        # with self.parking_info_lock:
        #   self.parking_info[msg_contents["lot_id"]] = msg_contents



        datetime_object = datetime.strptime(msg_contents["timestamp"], '%m/%d/%y %H:%M')
        lot_id = int(msg_contents["lot_id"])
        avail_spots = int(msg_contents["available_spots"])


        with self.my_lot_ids_lock:
          if lot_id not in self.my_lot_ids:
            self.my_lot_ids[lot_id] = True
            self.parking_info[lot_id] = {}
            self.most_recent_timestamp[lot_id] = datetime_object

        #Let parking_info have the data parsed for easier processing

        #Delete messages from exactly 4 hours ago
        # message_240_min_ago = datetime_object - timedelta(minutes=240)
        # message_245_min_ago = datetime_object - timedelta(minutes=245)
        # message_250_min_ago = datetime_object - timedelta(minutes=250)
        #
        #
        with self.parking_info_lock:
          self.parking_info[lot_id][datetime_object] = avail_spots
        #   if (message_240_min_ago in self.parking_info[lot_id]):
        #     del self.parking_info[lot_id][message_240_min_ago]
        #   if (message_245_min_ago in self.parking_info[lot_id]):
        #     del self.parking_info[lot_id][message_245_min_ago]
        #   if (message_250_min_ago in self.parking_info[lot_id]):
        #     del self.parking_info[lot_id][message_250_min_ago]

        with self.most_recent_timestamp_lock:
          if(datetime_object > self.most_recent_timestamp[lot_id]):
            self.most_recent_timestamp[lot_id] = datetime_object


        # "Sample" the data sometimes and send it to Mongo, with probability
        # of 1 / THRESHOLD

        #NOTE: Altered threshold to 1 because model is trained better when it has all the data

        THRESHOLD = 1.
        if random.uniform(0, 1) <= (1. / THRESHOLD):
          print ("Sampling this datapoint, adding to MongoDB...")
          # Use for when data hasn't been sorted, just downloaded from the internet
          # datetime_object = datetime.strptime(msg_contents["timestamp"], '%m/%d/%Y %I:%M:%S %p')

          # Use for when data has been sorted in Excel
          # datetime_object = datetime.strptime(msg_contents["timestamp"], '%m/%d/%y %H:%M')

          # lot_id = int(msg_contents["lot_id"])
          # avail_spots = int(msg_contents["available_spots"])
          #sensor_dao.add_sensor_data(lot_id, avail_spots, datetime_object)

        # Delete message so it doesn't stay in SQS for longer than necessary
        raw_msg.delete()

        # Show all messages
        sys.stdout.flush()
