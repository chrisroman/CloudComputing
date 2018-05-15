import boto3
import json
import os
import uuid
import threading
import time
import datetime
from app import my_lot_ids
from app.pcasts.dao import sensor_dao
import random

class S3Poller(object):
  """ Threading example class
  The run() method will be started and it will run in the background
  until the application exits.
  """

  def __init__(self, file_lock, model, model_lock):
    self.file_lock = file_lock
    self.model = model
    self.model_lock = model_lock
    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True                            # Daemonize thread
    print ("**************STARTING DAEMON")
    thread.start()                                  # Start the execution

  def run(self):
    """ Method that runs forever """
    ################################################
    #               Program start                  #
    ################################################
    print ("**************STARTED DAEMON")
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = response['Buckets']

    my_bucket_name = buckets[0]['Name']

    while True:
      #date = datetime.datetime.now().strftime("%Y-%m-%d")
      date = "2018-05-08"
      lot_ids = [0,1]
      for lot_id in lot_ids:
        print "Trying to store lot " + str(lot_id)
        model_name = 'ml_model_' + str(date) + "_" + str(lot_id) + '.txt'
        print model_name
        local_file_path = '/tmp/' + model_name
        #Change third argument to reflect local directory to store file
        with self.file_lock:
          s3.download_file(my_bucket_name, model_name, local_file_path)

        print "Reading file from S3..."
        with open(local_file_path) as file:
          temp = file.read()

          #parse text file
          model_raw_text = temp[1:-1]
          print "******************"
          print model_raw_text
          with self.model_lock:
            self.model[0] = [float(parameter) for parameter in model_raw_text.split(',')]
            print "S3 POLLER:model address" + str(hex(id(self.model[0])))
        print "Finished store lot " + str(lot_id)
      # Sleep for some time, so we don't constantly pull the model from S3
      print "SLEEEPING"
      time.sleep(30)
