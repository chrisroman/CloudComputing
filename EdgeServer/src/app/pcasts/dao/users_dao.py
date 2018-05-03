import datetime
from . import *

def get_all_users():
  return User.query.filter().all()
