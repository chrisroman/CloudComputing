import os

# Ensure Python path
basedir = os.path.abspath(os.path.dirname(__file__))

# Database info
RESERVATIONS_DB_USERNAME = os.environ['RESERVATIONS_DB_USERNAME']
RESERVATIONS_DB_PASSWORD = os.environ['RESERVATIONS_DB_PASSWORD']
RESERVATIONS_DB_HOST = os.environ['RESERVATIONS_DB_HOST']
RESERVATIONS_DB_NAME = os.environ['RESERVATIONS_DB_NAME']
RESERVATIONS_DB_URL = 'mysql://{}:{}@{}/{}?charset=utf8mb4'.format(
    RESERVATIONS_DB_USERNAME,
    RESERVATIONS_DB_PASSWORD,
    RESERVATIONS_DB_HOST,
    RESERVATIONS_DB_NAME
)

# Analog of database for testing purposes
TEST_RESERVATIONS_DB_USERNAME = os.environ.get('TEST_RESERVATIONS_DB_USERNAME')
TEST_RESERVATIONS_DB_PASSWORD = os.environ.get('TEST_RESERVATIONS_DB_PASSWORD')
TEST_RESERVATIONS_DB_HOST = os.environ.get('TEST_RESERVATIONS_DB_HOST')
TEST_RESERVATIONS_DB_NAME = os.environ.get('TEST_RESERVATIONS_DB_NAME')
TEST_RESERVATIONS_DB_URL = 'mysql://{}:{}@{}/{}?charset=utf8mb4'.format(
    TEST_RESERVATIONS_DB_USERNAME,
    TEST_RESERVATIONS_DB_PASSWORD,
    TEST_RESERVATIONS_DB_HOST,
    TEST_RESERVATIONS_DB_NAME
)


class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret"
  SECRET_KEY = "not_this"
  THREADS_PER_PAGE = 2

  # Mounting our DBs
  SQLALCHEMY_DATABASE_URI = RESERVATIONS_DB_URL

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = TEST_RESERVATIONS_DB_URL
