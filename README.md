# AWS EC2 And Webapp Automation

## Description
This automation runs with a single command and then responds with the AWS EC2 instance DNS name
that is hosting a custom Django webapp. 

## Design - Automation Step by Step 

This Python3 script first does the following on AWS

1. Sets up, or checks on VPC 
2. Checks security groups and add rules for TCP port 22 and port 80
3. Set up key-pairs and write .pem file to disk to be used for later access by script/user
4. Deploys an EC2 instance using the security groups, rules and keypairs

Then the Bash script does the following after fired from the Python script:
1. Connects to the EC2 instance using the .pem file
2. Sets up docker per dockers documentation over SSH
3. Uses Docker to run my custom Django webapp on port 80

## Installation

1. First grab a access key id / secret access key for AWS programmatic access [by reading this](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)
2. Clone this repo with ```git clone git@github.com:ispeakcomputer/auto_aws_ec3_webapp_deploy.git```
3. Run ```cd auto_aws_ec3_webapp_deploy ```to move into directory
4. Next run ```python3 -m venv venv ``` to create a virtual environment
5. Next run ```source venv/bin/activate```
6. Next Install all our requirements ```python3 -m pip install -r requirements.txt ``` 
7. Open **start_here.sh** and enter your keys and secrets from step 1 where you see **AWS_SECRET_ACCESS_KEY** and **AWS_ACCESS_KEY_ID**. Save and close.
8. Make the start script execute with ```chmod +x start_here.sh ```
9. Run the script with ```./start_here.sh```
10. Wait till the script finishes running and visit the DNS name of the Ec2 host it gives you in the browser. 
11. To run script again just run ```./start_here``` 

## Results

A tiny custom Django webapp with gif image I made will be hosted on the deployed Ec3 instance

![webapp](/images/webapp.png)

## Access Your Instance
Your private keys file with be saved to the current working directory. 

You can use ssh with the following command using the correct key file to login via SSH.

Find the key name, instance, and dns name in the log file within **deploy.log**

```ssh -i "key-pair-4756d380-b219-11eb-b0a7-a088b45856c8.pem" admin@<DNS NAME HERE>```
