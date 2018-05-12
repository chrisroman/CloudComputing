# Code adapted from https://gist.github.com/spandanb/cd023a79f0efbd00f929c14aa28ce5b2

import boto3
import pprint
import sys
import os
import time
from botocore.exceptions import ClientError

# Let's use Amazon ECS, EC2, and ELB
ecs_client = boto3.client('ecs')
ec2_client = boto3.client('ec2')
elb_client = boto3.client('elbv2')

def setup_mongo_cluster(**kwargs):
  print("\n============== STARTING '{}' CLUSTER ===============".format(kwargs["cluster_type"]))
  ret_val = {}

  create_instance = raw_input(
      ("Do you want to create an EC2 instance for "
        "{} cluster? (Note this is not an idempotent request) [y/n]: ".format(kwargs["cluster_type"])
      )
  )
  create_instance = True if create_instance == 'y' else False
  print("Create instance for mongo cluster? {}".format(create_instance))


  cluster_resp = ecs_client.create_cluster(
      clusterName=kwargs["cluster_name"]
  )
  print("Cluster Response: ")
  pprint.pprint(cluster_resp)
  print()

  # Create EC2 instance(s) in the cluster (only if specified to do so)
  # By default, your container instance launches into your default cluster.
  # If you want to launch into your own cluster instead of the default,
  # choose the Advanced Details list and paste the following script
  # into the User data field, replacing your_cluster_name with the name of your cluster.
  # !/bin/bash
  # echo ECS_CLUSTER=your_cluster_name >> /etc/ecs/ecs.config
  if (create_instance):
    instance_resp = ec2_client.run_instances(
        # Use the official ECS image (on us-east-1)
        ImageId="ami-aff65ad2",
        InstanceType="t2.micro",
        KeyName=kwargs["key_name"],
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[
            kwargs["sg_id"],
        ],
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + kwargs["cluster_name"] + " >> /etc/ecs/ecs.config",
    )
    print("Instance Response:")
    pprint.pprint(instance_resp)
    print()
    instance_id = instance_resp["Instances"][0]["InstanceId"]

    success = False
    while not success:
      try:
        # Associate this EC2 instance with the Elastic IP Address
        assoc_resp = ec2_client.associate_address(
            InstanceId=instance_id,
            PublicIp=kwargs["mongo_ip_addr"],
            AllowReassociation=True,
        )

        success = True

      except ClientError as e:
        print("The following error occurred: {}".format(e))
        if e.response["Error"]["Code"] == "InvalidInstanceID":
          print("Caught known exception InvalidInstanceID. Waiting for 10 seconds before retrying...")
          time.sleep(10)
        else:
          raise
    # endif

  # Create other service
  service_resp = ecs_client.create_service(
      cluster=kwargs["cluster_name"],
      serviceName=kwargs["service_name"],
      taskDefinition=kwargs["task_name"],
      desiredCount=kwargs["desired_count"],
      clientToken='request_identifier_string',
      launchType='EC2',
      deploymentConfiguration={
          'maximumPercent': 200,
          'minimumHealthyPercent': 50
      }
  )
  print("Service Response:")
  pprint.pprint(service_resp)
  print()




def setup_webserver_cluster(**kwargs):
  print("\n============== STARTING '{}' CLUSTER ===============".format(kwargs["cluster_type"]))
  ret_val = {}

  create_instance = raw_input(
      ("Do you want to create an EC2 instance for "
        "{} cluster? (Note this is not an idempotent request) [y/n]: ".format(kwargs["cluster_type"])
      )
  )
  create_instance = True if create_instance == 'y' else False
  print("Create instance for mongo cluster? {}".format(create_instance))


  cluster_resp = ecs_client.create_cluster(
      clusterName=kwargs["cluster_name"]
  )
  print("Cluster Response: ")
  pprint.pprint(cluster_resp)
  print()

  # Create EC2 instance(s) in the cluster (only if specified to do so)
  # By default, your container instance launches into your default cluster.
  # If you want to launch into your own cluster instead of the default,
  # choose the Advanced Details list and paste the following script
  # into the User data field, replacing your_cluster_name with the name of your cluster.
  # !/bin/bash
  # echo ECS_CLUSTER=your_cluster_name >> /etc/ecs/ecs.config
  if (create_instance):
    instance_resp = ec2_client.run_instances(
        # Use the official ECS image (on us-east-1)
        ImageId="ami-aff65ad2",
        InstanceType="t2.micro",
        KeyName=kwargs["key_name"],
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[
            kwargs["sg_id"],
        ],
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + kwargs["cluster_name"] + " >> /etc/ecs/ecs.config",
    )
    print("Instance Response:")
    pprint.pprint(instance_resp)
    print()


  # Create (or get) target group and associate it with the ALB and
  # the service that will be created
  tg_resp = elb_client.create_target_group(
      Name=kwargs["tg_name"],
      Protocol='HTTP',
      Port=kwargs["tg_port"],
      VpcId='vpc-cb6177b2', # DEFAULT for now
      HealthCheckProtocol='HTTP',
      HealthCheckPort='traffic-port',
      HealthCheckPath='/api/v1/hello/',
      Matcher={
          'HttpCode': '200'
      },
      TargetType='instance'
  )
  print("Target Group Response:")
  pprint.pprint(tg_resp)
  print()

  tg_arn = tg_resp["TargetGroups"][0]["TargetGroupArn"]


  # Add a rule to the main listener on the ALB to add the recently created
  # target group
  # Create (or get) the ALB
  alb_resp = elb_client.create_load_balancer(
      Name=kwargs["alb_name"],
      Subnets=[
          'subnet-580b2502',
          'subnet-88db7fec',
          'subnet-6df6c341',
          'subnet-4418f20f',
          'subnet-3f946e00',
          'subnet-be500cb2',
      ],
      SecurityGroups=[
          kwargs["sg_id"],
      ],
      Scheme='internet-facing',
      Type='application',
      IpAddressType='ipv4',
  )
  print("Load Balancer Response:")
  pprint.pprint(alb_resp)
  print()

  alb_arn = alb_resp["LoadBalancers"][0]["LoadBalancerArn"]


  # Create (or get) the listener for this ALB
  listener_resp = None
  try:
    listener_resp = elb_client.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            },
        ]
    )
  except ClientError as ex:
    # Most likely Received an error because the ALB Listener on port 80
    # already exists
    print(ex)
    listener_resp = elb_client.describe_listeners(
        LoadBalancerArn=alb_arn,
    )

  print("Listener Response:")
  pprint.pprint(listener_resp)
  print()

  listener_arn = listener_resp["Listeners"][0]["ListenerArn"]


  # Create the new rule that uses the recently created target group
  rule_resp = elb_client.create_rule(
      ListenerArn=listener_arn,
      Conditions=[
          {
              'Field': 'path-pattern',
              'Values': [
                  "/*",
              ]
          },
      ],
      Priority=1,
      Actions=[
          {
              'Type': 'forward',
              'TargetGroupArn': tg_arn
          },
      ]
  )
  print("Rule Response")
  pprint.pprint(rule_resp)
  print()

  # Create Task Definition for webserver service to use
  response = ecs_client.register_task_definition(
      family = "web_task",
      containerDefinitions = [
        {
          "name": "web_container",
          "image": "471709814231.dkr.ecr.us-east-1.amazonaws.com/cloudcomputing:webserver",
          "cpu": 400,
          "memory": 400,
          "portMappings": [
            {
              "hostPort": 0,
              "protocol": "tcp",
              "containerPort": 5000
            }
          ],
          "essential": True,
          "environment": [
            {
              "name": "EDGE_ALB_DNS",
              "value": kwargs["edge_alb_dns"]
            },
          ],
          "mountPoints": [],
          "volumesFrom": [],
        }
      ],
      volumes = [],
      placementConstraints = [],
      requiresCompatibilities = [
        "EC2"
      ],
      cpu = "400",
      memory = "400",
  )

  # Create webserver
  service_resp = ecs_client.create_service(
      cluster=kwargs["cluster_name"],
      serviceName=kwargs["service_name"],
      taskDefinition=kwargs["task_name"],
      loadBalancers=[
          {
              'targetGroupArn': tg_arn,
              'containerName': kwargs["container_name"],
              'containerPort': kwargs["container_port"]
          },
      ],
      desiredCount=kwargs["desired_count"],
      clientToken='request_identifier_string',
      launchType='EC2',
      deploymentConfiguration={
          'maximumPercent': 200,
          'minimumHealthyPercent': 50
      }
  )
  print("Service Response:")
  pprint.pprint(service_resp)
  print()






'''
  **kwargs:
    - key_name: (string) key name for SSH-ing into machine if necessary
    - sg_id: (string) Security group to give to EC2 instances (and ALB)
    - cluster_name: (string) Name of the cluster to create
    - mysql_ip_addr: (string) Elastic IP Address used for this instance
'''
def setup_mysql_server(**kwargs):
  cluster_resp = ecs_client.create_cluster(
      clusterName=kwargs["cluster_name"]
  )
  print("Cluster Response: ")
  pprint.pprint(cluster_resp)
  print()

  create_instance = raw_input(
      ("Do you want to create an EC2 instance for "
        "mysql cluster? (Note this is not an idempotent request) [y/n]: "
      )
  )
  create_instance = True if create_instance == 'y' else False
  print("Create instance for mysql cluster? {}".format(create_instance))
  if create_instance:
    success = False
    instance_resp = ec2_client.run_instances(
        # Use the official ECS image (on us-east-1)
        ImageId="ami-aff65ad2",
        InstanceType="t2.micro",
        KeyName=kwargs["key_name"],
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[
            kwargs["sg_id"],
        ],
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + kwargs["cluster_name"] + " >> /etc/ecs/ecs.config",
    )
    instance_id = instance_resp["Instances"][0]["InstanceId"]

    while not success:
      try:
        # Associate this EC2 instance with the Elastic IP Address
        assoc_resp = ec2_client.associate_address(
            InstanceId=instance_id,
            PublicIp=kwargs["mysql_ip_addr"],
            AllowReassociation=True,
        )

        success = True

      except ClientError as e:
        print("The following error occurred: {}".format(e))
        if e.response["Error"]["Code"] == "InvalidInstanceID":
          print("Caught known exception InvalidInstanceID. Waiting for 10 seconds before retrying...")
          time.sleep(10)
        else:
          raise
  # endif

  service_resp = ecs_client.create_service(
      cluster=kwargs["cluster_name"],
      serviceName=kwargs["service_name"],
      taskDefinition=kwargs["task_name"],
      desiredCount=kwargs["desired_count"],
      clientToken='request_identifier_string',
      launchType='EC2',
      deploymentConfiguration={
          'maximumPercent': 200,
          'minimumHealthyPercent': 50
      }
  )
  print("Service Response:")
  pprint.pprint(service_resp)
  print()

'''
  TODO: fix this INCOMPLETE documentation
  **kwargs:
    - cluster_name: (string) Name of the cluster to create
    - service_name: (string) Name of the service to create
    - task_name: (string) Name of the task definition to use (e.g. "edgetask0000:11")
    - key_name: (string) key name for SSH-ing into the machine in case of debugging needs
    - sg_id: (string) Security group to give to EC2 instances (and ALB)
    - container_name: (string) Name given to the container in task_name
    - container_port: (int) Port that the container will use (?)
    - alb_name: (string) Name for the ALB to create
    - tg_name: (string) Name for the target group to create
    - tg_port: (int) Port for which the target group will be placed
    - create_instance: (bool) Bool to create EC2 Instance or not
    - area_id: (int) ID for this area (if cluster_type == "edgeserver")
    - cluster_type: ("edgeserver"|"webserver"|"mongo"|"spark")
    - desired_count: (int) How many containers do you want to be run?
'''
def setup_edge_cluster(**kwargs):
  print("\n============== STARTING '{}' CLUSTER ===============".format(kwargs["cluster_type"]))

  ret_val = {}

  create_instance = raw_input(
      ("Do you want to create an EC2 instance for "
        "{} cluster? (Note this is not an idempotent request) [y/n]: ".format(kwargs["cluster_type"])
      )
  )
  create_instance = True if create_instance == 'y' else False
  print("Create instance for mongo cluster? {}".format(create_instance))


  cluster_resp = ecs_client.create_cluster(
      clusterName=kwargs["cluster_name"]
  )
  print("Cluster Response: ")
  pprint.pprint(cluster_resp)
  print()



  cluster_resp = ecs_client.create_cluster(
      clusterName=kwargs["cluster_name"]
  )
  print("Cluster Response: ")
  pprint.pprint(cluster_resp)
  print()


  # Create EC2 instance(s) in the cluster (only if specified to do so)
  # By default, your container instance launches into your default cluster.
  # If you want to launch into your own cluster instead of the default,
  # choose the Advanced Details list and paste the following script
  # into the User data field, replacing your_cluster_name with the name of your cluster.
  # !/bin/bash
  # echo ECS_CLUSTER=your_cluster_name >> /etc/ecs/ecs.config
  if (create_instance):
    instance_resp = ec2_client.run_instances(
        # Use the official ECS image (on us-east-1)
        ImageId="ami-aff65ad2",
        InstanceType="t2.micro",
        KeyName=kwargs["key_name"],
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[
            kwargs["sg_id"],
        ],
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + kwargs["cluster_name"] + " >> /etc/ecs/ecs.config",
    )
    print("Instance Response:")
    pprint.pprint(instance_resp)
    print()
  # endif


  setup_mysql_server(
      key_name = kwargs["key_name"],
      sg_id = kwargs["sg_id"],
      cluster_name = "mysql{}".format(str(kwargs["area_id"]).zfill(4)),
      mysql_ip_addr = kwargs["mysql_ip_addr"],
      service_name = "mysql_service",
      task_name = "mysql_task",
      desired_count = 1
  )

  # Create (or get) target group and associate it with the ALB and
  # the service that will be created
  tg_resp = elb_client.create_target_group(
      Name=kwargs["tg_name"],
      Protocol='HTTP',
      Port=kwargs["tg_port"],
      VpcId='vpc-cb6177b2', # DEFAULT for now
      HealthCheckProtocol='HTTP',
      HealthCheckPort='traffic-port',
      HealthCheckPath='/api/v1/hello/',
      Matcher={
          'HttpCode': '200'
      },
      TargetType='instance'
  )
  print("Target Group Response:")
  pprint.pprint(tg_resp)
  print()

  tg_arn = tg_resp["TargetGroups"][0]["TargetGroupArn"]


  # Add a rule to the main listener on the ALB to add the recently created
  # target group
  # Create (or get) the ALB
  alb_resp = elb_client.create_load_balancer(
      Name=kwargs["alb_name"],
      Subnets=[
          'subnet-580b2502',
          'subnet-88db7fec',
          'subnet-6df6c341',
          'subnet-4418f20f',
          'subnet-3f946e00',
          'subnet-be500cb2',
      ],
      SecurityGroups=[
          kwargs["sg_id"],
      ],
      Scheme='internet-facing',
      Type='application',
      IpAddressType='ipv4',
  )
  print("Load Balancer Response:")
  pprint.pprint(alb_resp)
  print()

  ret_val["edge_alb_dns"] = alb_resp["LoadBalancers"][0]["DNSName"]
  alb_arn = alb_resp["LoadBalancers"][0]["LoadBalancerArn"]


  # Create (or get) the listener for this ALB
  listener_resp = None
  try:
    listener_resp = elb_client.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            },
        ]
    )
  except ClientError as ex:
    # Most likely Received an error because the ALB Listener on port 80
    # already exists
    print(ex)
    listener_resp = elb_client.describe_listeners(
        LoadBalancerArn=alb_arn,
    )

  print("Listener Response:")
  pprint.pprint(listener_resp)
  print()

  listener_arn = listener_resp["Listeners"][0]["ListenerArn"]


  # Create the new rule that uses the recently created target group
  rule_resp = elb_client.create_rule(
      ListenerArn=listener_arn,
      Conditions=[
          {
              'Field': 'path-pattern',
              'Values': [
                  "/api/v1/area/{}".format(kwargs["area_id"]),
              ]
          },
      ],
      Priority=kwargs["area_id"] + 2,
      Actions=[
          {
              'Type': 'forward',
              'TargetGroupArn': tg_arn
          },
      ]
  )
  print("Rule Response")
  pprint.pprint(rule_resp)
  print()


  # Create task definition to be used for the service
  response = ecs_client.register_task_definition(
      family = kwargs["task_name"],
      containerDefinitions = [
        {
          "name": "edgecontainer",
          "image": "471709814231.dkr.ecr.us-east-1.amazonaws.com/cloudcomputing:edge_server",
          "cpu": 400,
          "memory": 400,
          "portMappings": [
            {
              "hostPort": 0,
              "protocol": "tcp",
              "containerPort": 5000
            }
          ],
          "essential": True,
          "environment": [
            {
              "name": "SERVER_ID",
              "value": str(kwargs["area_id"])
            },
            {
              "name": "RESERVATIONS_DB_HOST",
              "value": kwargs["mysql_ip_addr"]
            },
            {
              "name": "RESERVATIONS_DB_NAME",
              "value": os.environ['RESERVATIONS_DB_NAME']
            },
            {
              "name": "RESERVATIONS_DB_USERNAME",
              "value": os.environ['RESERVATIONS_DB_USERNAME']
            },
            {
              "name": "RESERVATIONS_DB_PASSWORD",
              "value": os.environ['RESERVATIONS_DB_PASSWORD']
            },
            {
              "name": "MONGO_ADDRESS",
              "value": kwargs["mongo_ip_addr"]
            },
          ],
          "mountPoints": [],
          "volumesFrom": [],
        }
      ],
      volumes = [],
      placementConstraints = [],
      requiresCompatibilities = [
        "EC2"
      ],
      cpu = "400",
      memory = "400",
  )

  # Create edgeservice
  # Info: Amazon ECS allows you to run and maintain a specified number
  # (the "desired count") of instances of a task definition
  # simultaneously in an ECS cluster.
  service_resp = ecs_client.create_service(
      cluster=kwargs["cluster_name"],
      serviceName=kwargs["service_name"],
      taskDefinition=kwargs["task_name"],
      loadBalancers=[
          {
              'targetGroupArn': tg_arn,
              'containerName': kwargs["container_name"],
              'containerPort': kwargs["container_port"]
          },
      ],
      desiredCount=kwargs["desired_count"],
      clientToken='request_identifier_string',
      launchType='EC2',
      deploymentConfiguration={
          'maximumPercent': 200,
          'minimumHealthyPercent': 50
      }
  )
  print("Service Response:")
  pprint.pprint(service_resp)
  print()

  return ret_val



if __name__ == "__main__":
  addr_resp = ec2_client.describe_addresses()
  sorted_ips = sorted([info["PublicIp"] for info in addr_resp["Addresses"]])
  NUM_TOPICS = 3

  setup_mongo_cluster(
      cluster_name = "mongo",
      service_name = "mongoservice",
      task_name = "mongo_task",
      key_name = "edgeclusterkey",
      sg_id = "sg-827063cb", # Group Name: http-ssh
      container_name = "mongo_container",
      container_port = 27017,
      mongo_ip_addr = sorted_ips[-1],
      cluster_type = "mongo",
      desired_count = 1,
  )

  egde_alb_dns = None

  # Launch the same number of clusters as there are areas
  for i in range(NUM_TOPICS):
    # Define cluster-specific settings
    ID_PADDING = 4
    area_id_str = str(i).zfill(ID_PADDING)
    cluster_name = "edgecluster{}".format(area_id_str)
    service_name = "edgeservice{}".format(area_id_str)
    task_name = "edgetask{}".format(area_id_str)
    tg_name = "area{}".format(area_id_str)
    area_id = i # The area id for which this cluster is responsible for

    resp = setup_edge_cluster(
        cluster_name = cluster_name,
        service_name = service_name,
        task_name = task_name,
        key_name = "edgeclusterkey",
        sg_id = "sg-827063cb", # Group Name: http-ssh
        container_name = "edgecontainer",
        container_port = 5000,
        alb_name = "edgealb",
        tg_name = tg_name,
        tg_port = 80,
        area_id = area_id,
        cluster_type = "edgeserver",
        desired_count = 2,
        mysql_ip_addr = sorted_ips[area_id],
        mongo_ip_addr = sorted_ips[-1],
    )

    edge_alb_dns = resp["edge_alb_dns"]

  setup_webserver_cluster(
      cluster_name = "webserver",
      service_name = "webservice",
      task_name = "web_task",
      key_name = "edgeclusterkey",
      sg_id = "sg-827063cb", # Group Name: http-ssh
      container_name = "web_container",
      container_port = 5000,
      alb_name = "webalb",
      tg_name = "web",
      tg_port = 80,
      cluster_type = "webserver",
      desired_count = 2,
      edge_alb_dns = edge_alb_dns,
  )





######################################################################
# DEAD CODE
######################################################################

# Shut everything down and delete task/service/instance/cluster
def terminate_ecs_example(cluster_name, service_name, task_name):
    try:
        # Set desired service count to 0 (obligatory to delete)
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=0
        )
        # Delete service
        response = ecs_client.delete_service(
            cluster=cluster_name,
            service=service_name
        )
        pprint.pprint(response)
    except:
        print("Service not found/not active")

    # Terminate virtual machine(s)
    response = ecs_client.list_container_instances(
        cluster=cluster_name
    )
    if response["containerInstanceArns"]:
        container_instance_resp = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=response["containerInstanceArns"]
        )
        for ec2_instance in container_instance_resp["containerInstances"]:
            ec2_termination_resp = ec2_client.terminate_instances(
                DryRun=False,
                InstanceIds=[
                    ec2_instance["ec2InstanceId"],
                ]
            )

    # Finally delete the cluster
    response = ecs_client.delete_cluster(
        cluster=cluster_name
    )
    pprint.pprint(response)
