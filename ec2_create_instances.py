#!/usr/bin/env python
# coding: utf-8
#
# Example code to create an EC2 instance
#
# In[1]:


from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import getpass
import subprocess
import time

# In[2]:


ec2 = boto3.resource('ec2','us-east-1')
dockerpass = getpass.getpass(prompt='Docker Password: ') 


# In[3]:


def show_instances(status):
    num = 0
    instances = ec2.instances.filter(
        Filters=[{'Name':'instance-state-name','Values':[status]}])
    if not instances:
        return num  # the list is empty
    for instance in instances:
        num = num + 1
        print(instance.id, instance.instance_type, instance.image_id, instance.public_ip_address, 
              instance.vpc_id)
    return num

# In[4]:
#create instances
with open('configurations.json') as json_file:
    data = json.load(json_file)
    for i in data['Instances']:
        if i['platform'] == 'aws':
            print('Name: ' + i['instance_name'])
            print('VM name: ' + i['VM_name'])
            print('VM Size ' + i['VM_size'])
            print('')

            if i['storage'] == 'Y':
                instances = ec2.create_instances(
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': i['instance_name']
                                },
                            ]
                        },
                    ],
                    BlockDeviceMappings=[
                        {
                            'DeviceName': '/dev/sdh',
                            'Ebs': {
                                'DeleteOnTermination': True,
                                'VolumeSize': i['storage_size'],
                                'VolumeType': 'standard'
                            }
                        },
                    ],
                    ImageId=i['VM_name'],
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=i['VM_size'],
                    KeyName=i['ssh_file']
                )
            else:
                instances = ec2.create_instances(
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': i['instance_name']
                                },
                            ]
                        },
                    ],
                    ImageId=i['VM_name'],
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=i['VM_size'],
                    KeyName=i['ssh_file']
                )
            print('instance created')
            for c in data['Containers']:
                if c['instance_name'] == i['instance_name']:
                    print("Adding " + c['docker_name'] + " to " + c['instance_name'])
                    #what docker should pull and run
                    if c['background'] == 'Y':
                        dockerRun = "run -td "
                    else:
                        dockerRun = "pull "
                    dockerRun = dockerRun + c['registry'] + '/' + c['docker_name']
                    #getting public dns name to ssh to
                    instance = instances[0]
                    instance.wait_until_running()  
                    instance.load()
                    dnsname = instance.public_dns_name

                    updateCommand = ""
                    installCommand = ""

                    if i['VM_name'] == "ami-0a887e401f7654935":
                        updateCommand = "yum -y update"
                        installCommand = "yum -y install docker"
                        dnsname = "ec2-user@" + dnsname
                        time.sleep(15) 
                    elif i['VM_name'] == "ami-0df6cfabfbe4385b7":
                        updateCommand = "zypper update"
                        installCommand = "zypper -n install docker"
                        dnsname = "ec2-user@" + dnsname 
                        time.sleep(30)
                    elif i['VM_name'] == "ami-07ebfd5b3428b6f4d":
                        updateCommand = "apt update"
                        installCommand = "apt install docker.io -y"
                        dnsname = "ubuntu@" + dnsname
                        time.sleep(15)
                    elif i['VM_name'] == "ami-0e2ff28bfb72a4e45":
                        updateCommand = "yum -y update"
                        installCommand = "yum install docker -y"  
                        dnsname = "ec2-user@" + dnsname
                        time.sleep(20)
                    elif i['VM_name'] == "ami-0c322300a1dd5dc79":
                        updateCommand = "yum -y update"
                        installCommand = "yum -y install docker"
                        dnsname = "ec2-user@" + dnsname
                        time.sleep(15)

                
                    callstring = "./load-docker.sh \"" + dnsname + "\" \"" + updateCommand + "\" \"" + installCommand + "\" \"" + dockerpass + "\" \"" + dockerRun + "\""
                    
                    subprocess.call(callstring, shell=True)
                
        


# In[9]:


print("Creating EC2 instance(s)...")


# In[10]:


ret = show_instances('pending')
print("pending = ", ret)


# In[11]:


ret = show_instances('running')
print("running = ", ret)

