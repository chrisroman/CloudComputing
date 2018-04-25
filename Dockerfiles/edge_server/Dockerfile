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
RUN rm -rf $START_DIR/testing/

# Upgrade pip
RUN pip install -U pip

# Install required python packages
RUN pip install -r $START_DIR/requirements.txt

CMD python $START_DIR/edge_server.py
