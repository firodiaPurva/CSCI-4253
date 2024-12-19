#!/bin/bash

# Log output to a file
exec > /var/log/flask_setup.log 2>&1

# Update the package list
sudo apt-get update

# Install necessary packages
sudo apt-get install -y python3 python3-pip git

# Clone the Flask tutorial repository
git clone https://github.com/cu-csci-4253-datacenter/flask-tutorial

# Navigate into the cloned repository
cd flask-tutorial

# Install the package
sudo python3 setup.py install
sudo pip3 install -e .

# Set the Flask app environment variable
export FLASK_APP=flaskr

# Initialize the database
flask init-db

# Run the Flask application in the background
nohup flask run -h 0.0.0.0 &
