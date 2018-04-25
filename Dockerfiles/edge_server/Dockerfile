FROM python:2.7

# Copy over our requirements.txt file
COPY EdgeServer/requirements.txt /tmp/

# Copy over our app code
COPY EdgeServer/ /root

# Upgrade pip
RUN pip install -U pip

# Install required python packages
RUN pip install -r /tmp/requirements.txt

CMD ["python", "/root/edge_server.py"]
