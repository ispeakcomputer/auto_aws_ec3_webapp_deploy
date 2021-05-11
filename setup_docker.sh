#!/bin/bash
_remote=$1
_keypair_name=$2

if [ -z "$1" ]
then
    echo -e "\e[31mNo argument supplied to bash script - Enter IP/DNS of EC2 Instance\e[0m"
elif [ -z "$2" ]
then
    echo -e "\e[31mNo argument supplied to bash script. Keypair name missing from 2 postional argument\e[0m"
else

echo -e "\e[95m*** Shell script waiting for SSH to run on host***\e[0m"
# sleep because SSH isn't running
sleep 60

echo -e "\e[95m*** Running commands on remote host named $_remote ***\e[0m"

ssh -o "StrictHostKeyChecking=no" -i "$_keypair_name" -T admin@$_remote <<'EOL'
sudo apt-get update -y

sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release --yes

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io --yes

sudo docker run -d -p 80:8000 ispeakcomputer/sampleapp

exit
EOL

fi
