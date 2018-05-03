FROM tiangolo/uwsgi-nginx-flask:python2.7

# Copy over our requirements.txt file
COPY Server/requirements.txt /tmp/

# Upgrade pip
RUN pip install -U pip

# Install appdev dependencies
RUN pip install git+https://github.com/cuappdev/appdev.py.git#egg=appdev.py

# Install required python packages
RUN pip install -r /tmp/requirements.txt

# Export environment variables
ENV DB_USERNAME "CHANGEME"
ENV DB_PASSWORD "CHANGEME"
ENV DB_HOST "localhost"
ENV DB_NAME "pcasts_db_dev"
ENV TEST_DB_USERNAME "CHANGEME"
ENV TEST_DB_PASSWORD "CHANGEME"
ENV TEST_DB_HOST "localhost"
ENV TEST_DB_NAME "test_pcasts_db_dev"
ENV APP_SETTINGS "config.ProductionConfig"

# Copy over our app code
COPY Server/src /app
