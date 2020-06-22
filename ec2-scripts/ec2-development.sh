#!/usr/bin/bash

# Install packages
sudo yum -y update
sudo yum install -y emacs-nox nano tree python3
sudo amazon-linux-extras install -y java-openjdk11
sudo yum install -y java-11-openjdk-devel
sudo yum install -y git


# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/hootskoot/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"


# Start/enable services
sudo systemctl stop postfix
sudo systemctl disable postfix
