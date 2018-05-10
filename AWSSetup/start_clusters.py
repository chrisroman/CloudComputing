# Code adapted from https://gist.github.com/spandanb/cd023a79f0efbd00f929c14aa28ce5b2

import boto3
import pprint
import sys
from botocore.exceptions import ClientError

# Let's use Amazon ECS, EC2, and ELB
ecs_client = boto3.client('ecs')
ec2_client = boto3.client('ec2')
elb_client = boto3.client('elbv2')


'''
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
def setup_cluster(**kwargs):
  print("\n============== STARTING '{}' CLUSTER ===============".format(kwargs["cluster_type"]))
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
  if (kwargs["create_instance"]):
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

  if kwargs["cluster_type"] == "edgeserver":
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
  else:
    # Create other service
    # Info: Amazon ECS allows you to run and maintain a specified number
    # (the "desired count") of instances of a task definition
    # simultaneously in an ECS cluster.
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
  # endif



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

if __name__ == "__main__":
  # Launch the same number of clusters as there are areas
  for i in range(3):
    # Define cluster-specific settings
    create_instance = raw_input(
        ("Do you want to create an EC2 instance for "
          "cluster {}? (Note this is not an idempotent request) [y/n]: "
        ).format(i)
    )
    create_instance = True if create_instance == 'y' else False
    print("Create instance for cluster {}? {}".format(i, create_instance))

    ID_PADDING = 4
    area_id_str = str(i).zfill(ID_PADDING)
    cluster_name = "edgecluster{}".format(area_id_str)
    service_name = "edgeservice{}".format(area_id_str)
    task_name = "edgetask{}".format(area_id_str)
    tg_name = "area{}".format(area_id_str)
    area_id = i # The area id for which this cluster is responsible for

    setup_cluster(
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
        create_instance = create_instance,
        area_id = area_id,
        cluster_type = "edgeserver",
        desired_count = 2
    )

  create_instance = raw_input(
      ("Do you want to create an EC2 instance for "
        "mongo cluster? (Note this is not an idempotent request) [y/n]: "
      )
  )
  create_instance = True if create_instance == 'y' else False
  print("Create instance for mongo cluster? {}".format(create_instance))
  # Setup Mongo Cluster
  setup_cluster(
      cluster_name = "mongo",
      service_name = "mongoservice",
      task_name = "mongo_task",
      key_name = "edgeclusterkey",
      sg_id = "sg-827063cb", # Group Name: http-ssh
      container_name = "mongo_container",
      container_port = 27017,
      create_instance = create_instance,
      area_id = area_id,
      cluster_type = "mongo",
      desired_count = 1
  )

  # terminate_ecs_example(cluster_name, service_name, task_name)
