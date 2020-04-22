#!/bin/bash

az vm create --resource-group cis4010_rg --location canadacentral --name $1 --image $2 --size $3 $4 $5 --generate-ssh-keys
