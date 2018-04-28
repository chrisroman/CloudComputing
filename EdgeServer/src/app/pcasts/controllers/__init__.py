from flask import request, render_template, jsonify, redirect
from appdev.controllers import *
from app.pcasts.dao import users_dao
from app.pcasts.dao import sensor_dao
from app.pcasts.dao import customers_dao


from app.pcasts.models._all import *

# Serializers
# user_schema = UserSchema()
