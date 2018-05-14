FROM python:2.7
RUN apt-get update && apt-get install -y git

# Upgrade pip
RUN pip install -U pip

# Copy AWS credentials
COPY .aws/ /root/.aws/

# Export necessary environment variables
ENV RESERVATIONS_DB_USERNAME "CHANGEME"
ENV RESERVATIONS_DB_PASSWORD "CHANGEME"
ENV RESERVATIONS_DB_HOST "localhost"
ENV RESERVATIONS_DB_NAME "pcasts_db_dev"
ENV TEST_RESERVATIONS_DB_USERNAME "CHANGEME"
ENV TEST_RESERVATIONS_DB_PASSWORD "CHANGEME"
ENV TEST_RESERVATIONS_DB_HOST "localhost"
ENV TEST_RESERVATIONS_DB_NAME "test_pcasts_db_dev"
ENV APP_SETTINGS "config.ProductionConfig"

# Clone project directory
RUN git clone https://github.com/chrisroman/CloudComputing.git /CloudComputing

ENV START_DIR=/CloudComputing/EdgeServer
WORKDIR $START_DIR

# Remove files that take up lots of space for no reason, but must still
# be included in the github repo
RUN rm -rf /CloudComputing/testing

# Install required packages
RUN $START_DIR/setup_environment.sh

# Do the following when the container starts running:
# - Pull the most recent version of the project from Github
# - Install any potential new packages
# - Run the flask server
CMD cd $START_DIR && \
git pull origin master && \
pip install -r $START_DIR/requirements.txt && \
python $START_DIR/src/main.py
