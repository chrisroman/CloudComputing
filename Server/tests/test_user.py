import json
import config
import requests
from app import constants


class TestUser(object):

  def __init__(self, **kwargs):
    self.name = kwargs.get('name', '')
    self.test_client = kwargs.get('test_client')
    self.uid = kwargs.get('uid', None)

  def post(self, url, data=None):
    response = self.test_client.post(url)
    return response

  def get(self, url, data=None):
    response = self.test_client.get(url, headers=header)
    return response

  def delete(self, url, data=None):
    response = self.test_client.delete(url, headers=header)
    return response
