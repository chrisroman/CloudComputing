import boto3
from app.pcasts.models._all import *
from app.pcasts.utils import mysql_db_utils

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
reservations = dynamodb.Table('Reservations')
