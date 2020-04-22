#!/usr/bin/env python
# coding: utf-8

import subprocess
import json
import time
import getpass
import os

dockerpass = getpass.getpass(prompt='Docker Password: ') 

def installDocker(callstring):
    try:
        subprocess.call(callstring, shell=True, timeout=300)
    except:
        installDocker(callstring)

with open('configurations.json') as json_file:
    data = json.load(json_file)
    for i in data['Instances']:
        if i['platform'] == 'azure':
            print('Name: ' + i['instance_name'])
            print('VM name: ' + i['VM_name'])
            print('')

            callstring = "./az_makeVM.sh " + i['instance_name'] + " " + i['VM_name'] + " " + i['VM_size']
            if i['storage'] == 'Y':
                callstring = callstring + " --data-disk-sizes-gb " + str(i['storage_size'])
            subprocess.call(callstring, shell=True)

            for c in data['Containers']:
                if c['instance_name'] == i['instance_name']:
                    print("Adding " + c['docker_name'] + " to " + c['instance_name'])
                    #what docker should pull and run
                    if c['background'] == 'Y':
                        dockerRun = "run -td "
                    else:
                        dockerRun = "pull "
                    dockerRun = dockerRun + c['registry'] + '/' + c['docker_name']


                    #dnsjson = subprocess.run(['az', 'vm', 'list-ip-addresses', '-g', 'cis4010_rg', '-n', i['instance_name']], shell=True, capture_output=True)
                    subprocess.call("az vm show -g cis4010_rg --name " + i['instance_name'] + " -d > tempAZ.json", shell=True)
                    with open('tempAZ.json') as json_file:
                        dnsjson = json.load(json_file)
                        dnsname = "sam@" + dnsjson['publicIps']

                    updateCommand = "apt update"
                    installCommand = "apt install docker.io -y"
                    time.sleep(15)

                    callstring = "./az-docker.sh \"" + dnsname + "\" \"" + updateCommand + "\" \"" + installCommand + "\" \"" + dockerpass + "\" \"" + dockerRun + "\""
            
                    installDocker(callstring)
            
                    os.remove("tempAZ.json")





