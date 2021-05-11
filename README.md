# AWS EC2 And Webapp Automation

## Description
This automation runs with a single command and then responds with the AWS EC2 instance DNS name
that is hosting a custom Django webapp. 

## Design - Step by Step

This Python3 script first does the following on AWS

1. Sets up, or checks on VPC 
2. Checks security groups and add rules for TCP port 22 and port 80
3. Set up key-pairs and write .pem file to disk to be used for later access by script/user
4. Deploys an EC2 instance using the security groups, rules and keypairs

Then the Bash script does following:
1. Connects to the EC2 instance using the .pem file
2. Sets up docker per dockers documentation over SSH
3. Uses Docker to run my custom Django webapp on port 80

## Installation

1. First grab a access key id / secret access key for AWS programmatic access [by reading this](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)
2. Next run ```python3 -m venv venv ``` to create a virtual environment
3. Next run ```source venv/bin/activate```
4. Next Install all our requirements ```python3 -m pip install -r requirements.txt ``` 
5. Run ```python3 -m awscli configure``` and enter your keys and secrets from step 1.
6. Make the start script execute with ```chmod +x start_here.sh ```
7. Run the script with ```./start_here.sh```
8. Wait till the script finishes running and visit the DNS name of the Ec2 host it gives you in the browser.

## Results

A tiny custom Django webapp with gif image I made will be hosted on the deployed Ec3 instance

![webapp](/images/webapp.png)

## Access Your Instance
Your private keys file with be saved to the current working directory. 

You can use ssh with the following command using the correct key file to login via SSH.

```ssh -i "key-pair-4756d380-b219-11eb-b0a7-a088b45856c8.pem" admin@<DNS NAME HERE>```
