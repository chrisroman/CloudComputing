import boto3
import json
import os
import uuid
import threading
import time
import datetime
from app.pcasts.dao import sensor_dao
import random

class S3Poller(object):
  """ Threading example class
  The run() method will be started and it will run in the background
  until the application exits.
  """

  def __init__(self, file_lock):
    self.file_lock = file_lock
    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

  def run(self):
    """ Method that runs forever """
    ################################################
    #               Program start                  #
    ################################################
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = response['Buckets']

    my_bucket_name = buckets[0]['Name']

    while True:
      date = datetime.datetime.now().strftime("%Y-%m-%d")
      model_name = 'ml_model_' + date + '_.txt'
      local_file_path = '/tmp/' + model_name

      #Change third argument to reflect local directory to store file 
      with self.file_lock:
        s3.download_file(my_bucket_name, model_name, local_file_path)

      print "Reading file from S3..."
      with open(local_file_path) as file:
        print file.read()

      # Sleep for some time, so we don't constantly pull the model from S3
      time.sleep(120)

