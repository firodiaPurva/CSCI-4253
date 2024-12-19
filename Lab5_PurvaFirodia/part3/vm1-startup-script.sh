#!/bin/bash

# Log output to a file
exec > /var/log/vm1_startup_script.log 2>&1

# Update the package list
sudo apt-get update

# Install python3-pip
sudo apt-get install -y python3-pip

# Upgrade Google API client libraries
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Download VM-2 creation script from metadata
curl http://metadata/computeMetadata/v1/instance/attributes/vm2-startup-script -H "Metadata-Flavor: Google" -o vm2_startup_script.sh

# Download VM-2 launch code
curl http://metadata/computeMetadata/v1/instance/attributes/vm2-create-code -H "Metadata-Flavor: Google" -o vm2-launch-code.py

# Provide necessary credentials
curl http://metadata/computeMetadata/v1/instance/attributes/service-credentials -H "Metadata-Flavor: Google" -o service-credentials.json

# Set Google Cloud Project environment variable
export GOOGLE_CLOUD_PROJECT="myprojectlab5-437623"  # Updated project ID

# Run the VM-2 creation Python script
python3 vm2-launch-code.py
