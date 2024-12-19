#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

#
# Use Google Service Account - See https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
#

credentials, PROJECT = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

vm1_startup_script = open(os.path.join(os.path.dirname(__file__), "vm1-startup-script.sh")).read()
vm2_startup_script = open(os.path.join(os.path.dirname(__file__), "vm2-startup-script.sh")).read()
vm2_create_code = open(os.path.join(os.path.dirname(__file__), "vm1-create-vm2-code.py")).read()
service_account_credentials = open(os.path.join(os.path.dirname(__file__), "service-credentials.json")).read()

def wait_for_operation(
    compute: object,
    project: str,
    zone: str,
    operation: str,
) -> dict:
    """Waits for the given operation to complete.

    Args:
      compute: an initialized compute service object.
      project: the Google Cloud project ID.
      zone: the name of the zone in which the operation should be executed.
      operation: the operation ID.

    Returns:
      The result of the operation.
    """
    print("Waiting for operation to finish...")
    while True:
        result = (
            compute.zoneOperations()
            .get(project=project, zone=zone, operation=operation)
            .execute()
        )

        if result["status"] == "DONE":
            print("done.")
            if "error" in result:
                raise Exception(result["error"])
            return result

# Function to create an instance with the given parameters
def create_instance(compute, project, zone, name, machine_type, source_disk_image, startup_script, vm2_startup_script, vm2_create_code, service_credentials):
    config = {
        'name': name,
        'machineType': f"zones/{zone}/machineTypes/{machine_type}",
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],
        'networkInterfaces': [
            {
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }
        ],
        "metadata": {
            "items": [
                {"key": "startup-script", "value": startup_script},
                {"key": "vm2-startup-script", "value": vm2_startup_script},
                {"key": "vm2-create-code", "value": vm2_create_code},
                {"key": "service-credentials", "value": service_credentials},
                {"key": "project", "value": project}
            ]
        },
        'tags': {
            'items': ['allow-5000']  # Wrap tags in an 'items' list
        }
    }

    return compute.instances().insert(project=project, zone=zone, body=config).execute()

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

def main(project, zone, instance_name):
    # Set the parameters for the new instance
    machine_type = 'f1-micro'  # f1-micro is part of the "free tier"
    source_disk_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"  # Ubuntu 22.04 LTS image

    # Create the instance
    print(f"Creating instance {instance_name} in {zone}...")
    operation = create_instance(service, project, zone, instance_name, machine_type, source_disk_image, vm1_startup_script, vm2_startup_script, vm2_create_code, service_account_credentials)
    wait_for_operation(service, project, zone, operation["name"])

    # List running instances after creation
    print("Your running instances are:")
    instances = list_instances(service, project, zone)
    if instances:
        for instance in instances:
            print(instance['name'])
    else:
        print("No running instances found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", default="myprojectlab5-437623", help="Your Google Cloud project ID.")
    parser.add_argument(
        "--zone", default="us-west1-b", help="Compute Engine zone to deploy to."
    )
    parser.add_argument("--name", default="myprojectlab5-p3-1", help="New instance name.")

    args = parser.parse_args()

    main(args.project_id, args.zone, args.name)
