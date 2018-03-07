import unittest
import os
import sys
from tests.test_user import *

class TestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()
    self.user1 = TestUser(test_client=self.app)

  def tearDown(self):
    pass
