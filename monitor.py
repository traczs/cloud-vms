#!/usr/bin/env python
# coding: utf-8

import boto3
import subprocess
import json

ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print("")
    print(instance.id, instance.instance_type, instance.image_id, instance.public_ip_address, 
              instance.vpc_id)

    if instance.image_id == "ami-07ebfd5b3428b6f4d":
        dnsname = "ubuntu@" + instance.public_dns_name
    else:
        dnsname = "ec2-user@" + instance.public_dns_name
    
    callstring = "ssh -i \"ec2-1-keypair.pem\" " + dnsname + " \"echo 'installed images:';sudo docker images; echo 'running containers:'; sudo docker ps; echo 'all containers:'; sudo docker ps -a\""
    subprocess.call(callstring, shell=True)

subprocess.call("az vm list -d --query \"[?powerState=='VM running']\" > tempAZ.json", shell=True)
with open('tempAZ.json') as json_file:
    json = json.load(json_file)
    for vm in json:
        print("")
        print(vm['name'], vm['storageProfile']['imageReference'])
        callstring = "ssh sam@" + vm['publicIps'] + " \"echo 'installed images:';sudo docker images; echo 'running containers:'; sudo docker ps; echo 'all containers:'; sudo docker ps -a\""
        subprocess.call(callstring, shell=True)