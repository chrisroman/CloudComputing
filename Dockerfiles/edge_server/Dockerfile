FROM python:2.7
RUN apt-get update && apt-get install -y git

# Clone project directory
RUN git clone https://github.com/chrisroman/CloudComputing /CloudComputing

# Copy AWS credentials
COPY .aws/ /root/.aws/

ENV START_DIR=/CloudComputing/EdgeServer
WORKDIR $START_DIR

# Remove files that take up lots of space for no reason, but must still
# be included in the github repo
RUN rm -rf /CloudComputing/testing

# Upgrade pip
RUN pip install -U pip

# Install required packages
RUN $START_DIR/setup_environment.sh

# On startup of Docker container, run the server
CMD python $START_DIR/src/main.py
