#!/bin/bash

#azure ssh

#ssh $1 "sudo $2; logout" 

#ssh $1 "sudo $3; logout"

#ssh $1 "sudo service docker start; sudo docker login -u traczs -p $4; logout"

#ssh $1 "sudo docker $5"

ssh $1 "sudo $2; sudo $3; sudo service docker start; sudo docker login -u traczs -p $4; sudo docker $5"
