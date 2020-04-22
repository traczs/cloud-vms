#!/bin/bash

#aws

#linux 2 (yum)
#ssh -i "ec2-1-keypair.pem" ec2-user@ec2-3-88-255-179.compute-1.amazonaws.com
#sudo yum update -y
#sudo yum install docker -y

#SUSE
#ssh -i "ec2-1-keypair.pem" ec2-user@ec2-54-162-183-184.compute-1.amazonaws.com
#sudo zypper -n install docker

#ubuntu
#ssh -i "ec2-1-keypair.pem" ubuntu@ec2-18-208-198-122.compute-1.amazonaws.com
#sudo apt install docker.io -y

#linux ami
#ssh -i "ec2-1-keypair.pem" ec2-user@ec2-34-207-197-33.compute-1.amazonaws.com
#sudo yum install docker -y

#redhat
#ssh -i "ec2-1-keypair.pem" ec2-user@ec2-3-84-245-167.compute-1.amazonaws.com
#sudo yum install docker -y



ssh -i "ec2-1-keypair.pem" $1 "sudo $2; sudo $3; sudo service docker start; sudo docker login -u traczs -p $4; sudo docker $5" 
#sudo $2
#sudo service docker start
#sudo docker login -u traczs -p $3
#sudo docker pull $4
