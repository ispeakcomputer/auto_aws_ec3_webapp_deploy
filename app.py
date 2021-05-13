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
                                                 level=logging.INFO)

keypair_id = "key-pair"
UID = uuid.uuid1()
keypair_name = keypair_id + "-" + str(UID)

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
            logging.info("key created ->" + keypair_name + ".pem")
            return keypair_name
    
    """Update Security Group of EC2 instance"""
    def setup_security_group(self):
        response = self.client.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        try:    
            response = self.client.create_security_group(GroupName='SECURITY_GROUP_NAME',
                                                    Description='DESCRIPTION',
                                                    VpcId=vpc_id)
            security_group_id = response['GroupId']
            logging.info("Security Group Created %s in vpc %s." % (security_group_id, vpc_id))
            data = self.client.authorize_security_group_ingress(
                                                    GroupId=security_group_id,
                                                    IpPermissions=[
                                                    {'IpProtocol': 'tcp',
                                                    'FromPort': 80,
                                                    'ToPort': 80,
                                                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                                                    {'IpProtocol': 'tcp',
                                                    'FromPort': 22,
                                                    'ToPort': 22,
                                                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                                                    ])
            logging.info('Ingress Successfully Set %s' % data)
        except ClientError as e:
            logging.error(e)
        except InvalidGroup.Duplicate as e:
            logging.info(e)
            
    """Create EC2 instance"""
    def create_ec2_instance(self):
        
        try:
            response = self.ec2.create_instances(ImageId='ami-0528712befcd5d885',
                                            MinCount=1, 
                                            MaxCount=1,
                                            InstanceType='m1.small',
                                            KeyName=keypair_name)
        except botocore.exceptions.ClientError as e:
            logging.error("Key pair didn't create before launching EC2 Instance")
        
        try:
            instance_id = response[0].instance_id
            logging.info("Created instance - instance id : " + str(instance_id))
            
            instance = response[0]
            instance.wait_until_running()
            # Reload the instance attributes
            instance.load()
            logging.info("Instance now fully loaded and DNS name is : " + str (instance.public_dns_name))
            
            return instance.public_dns_name 
        except NameError:
            logging.error("No response from ec2 object. Something went wrong, try again")
        
    """Run Simple Shell Script To Install Docker and Run"""
    def shell_script_webapp_deploy(self, keypair_name, dns_name):
        try:        
            subprocess.run(["chmod", "+x", "setup_docker.sh"])
            key_file = str(keypair_name) + ".pem"
            subprocess.run(["./setup_docker.sh", str(dns_name), key_file])
            
            logging.info("Please View App At : " + str(dns_name))
            return True
        except:
            logging.error("Something went wrong with shell script. Check instance dns name and keypairs")
            return False

if __name__ == "__main__":

    aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
    
    if not aws_secret and aws_key:
            print('\033[31m' + 'Please enter your aws secret and key. ')
            print('\033[39m')
    else:
            print('\033[95m' + ' *Setting up, and checking VPC, Security groups and rules, key-pairs and EC2 instance. Please wait*')
            print('\033[39m')
        
            try:
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
            
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'AuthFailure':
                    print('\033[31m' + 'Your AWS creds are incorrect. Replace and try again ')
                    print('\033[39m')
