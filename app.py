import botocore
from botocore.exceptions import ClientError
import boto3
import os
import subprocess
import uuid
import logging

logging.basicConfig(handlers=[logging.FileHandler(filename="deploy.log", 
                                                 encoding='utf-8', mode='w')],
                                                 format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                                                 datefmt="%F %A %T", 
                                                 level=logging.DEBUG)

keypair_id = "key-pair"
UID = uuid.uuid1()
keypair_name = keypair_id + "-" + str(UID)
#key= os.environ['AWS_SECRET_ACCESS_KEY']
#secret = os.environ['AWS_ACCESS_KEY_ID']
#aws_region = os.environ['YOUR_AWS_REGION']

class Deployer:
    def __init__(self):
        self.client = boto3.client('ec2')
        self.ec2 = boto3.resource('ec2')
    
    """Check for and make default VPC for Ec2 Instance"""
    def vpc_deployer(self):
        try:
            self.client.create_default_vpc()
        except:
            logging.info("VPC exists already for EC2 Instance")
     
    """Check For Key-pair"""
    def keypair_deployer(self): 
        try:
            keys_response = self.client.describe_key_pairs(KeyNames=[keypair_name])
            return keys_response
        except botocore.exceptions.ClientError as e:
            logging.info("Key doesn't exist. Create a new one")
            keys_response = False
            return keys_response
    
    """Create and save keypair to file"""
    def private_key_saver(self, keys_response):          
        if keys_response:
            logging.info("key pair is in place already")
        else:
            keypair = self.client.create_key_pair(KeyName=keypair_name)
            private_key = keypair["KeyMaterial"]
            with os.fdopen(os.open( keypair_name + ".pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
                    handle.write(private_key)
            logging.info("key created")
            return keypair_name
    

if __name__ == "__main__":

    print('\033[95m' + ' *Setting up, and checking VPC, Security groups and rules, key-pairs and EC2 instance. Please wait*')
    print('\033[39m')

    deployer = Deployer()
    deployer.vpc_deployer()
    keys_response = deployer.keypair_deployer()
    keypair_name = deployer.private_key_saver(keys_response)
    deployer.setup_security_group()
    dns_name = deployer.create_ec2_instance()
    execution = deployer.shell_script_webapp_deploy(keypair_name,dns_name)
    
    if execution:
        print('\033[95m' + ' *Visit The Deployed Webapp Here --> ' + str(dns_name))
        print('\033[39m')
    else:
        print('\033[31m' + 'Shell Script had issues. Check logs for more details or try again because ssh didn not respond')
        print('\033[39m')
