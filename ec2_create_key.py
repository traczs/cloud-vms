#!/usr/bin/env python
# coding: utf-8
#
# Example code to create an EC2 instance
#
# In[1]:


from __future__ import print_function # Python 2/3 compatibility
import boto3


# In[2]:


ec2 = boto3.resource('ec2','us-east-1')



# Create a file to store the key locally
# In[4]:


outfile = open('ec2-1-keypair.pem','w')

# Call the boto ec2 function to create a key pair
# In[5]:


key_pair = ec2.create_key_pair(KeyName='ec2-1-keypair')


# In[6]:


# Capture the key and store it in a file


# In[7]:


KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)