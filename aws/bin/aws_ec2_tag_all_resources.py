#!/usr/bin/env python3

from datetime import datetime
import argparse
import logging
import sys
from AWS import AWS

### PARSE ARGUMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dept', 
    help='Name of dept. Must be one of: chips, cloud, it, or rnd',  
    metavar=''
)
args = parser.parse_args()

### LOGGER FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
logging.basicConfig(
    filename=f'../log/{datetime.now().strftime("%Y-%m-%d-%H:%M")}-aws-ec2-tag-all-resources.log', 
    filemode='w', 
    format='%(message)s',
  level=logging.INFO
)
# Print all logs to screen
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.info(f'aws_ec2_tag_all_resources.py ==> TAGGING ALL EC2 RESOURCES\n')

### MAIN FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AWS = AWS()
# Get a list of all departments
departments = ['chips', 'cloud', 'it', 'rnd']
tags = {
            'chips': { 'Owner': 'jclark@quantum-si.com'  },
            'cloud': { 'Owner': 'sliu@quantum-si.com'    },
            'it':    { 'Owner': 'mamey@quantum-si.com'   },
            'rnd':   { 'Owner': 'galppay@quantum-si.com' }
        }

# Get a list of all AMIs
images = AWS.getImages()
logging.debug(f'getImages() ==> { images }')
logging.info(f'getImages() ==> Retrieved {len(images)} AMIs')

# Get a list of all resources in each department's EC2 resource group
for dept in departments: 
    logging.info(f'aws_ec2_tag_all_resources.py ==> Tagging resources for {dept}')

    instances = AWS.getEc2Resources(dept)
    if instances:
        logging.debug(f'getEc2Resources() ==> {instances}')
        logging.info(f'getEc2Resources() ==> Found {len(instances)} {dept} instances\n')

        for i in instances:
            instanceId = i.split('/')[1]
            instance = AWS.getInstance(instanceId)
            if not instance: 
                logging.warning(f'getInstance() ==> Instance { instanceId } not found. Skipping...\n\n')
                continue

            ## TAG INSTANCE 
            logging.info(f'aws_ec2_tag_all_resources.py ==> Tagging { instanceId }...')
            logging.info(f"Current Tags ==> { instance['Tags'] }")

            instanceTags = {}
            Name = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in instance else None
            Owner = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in instance else None
            Department = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in instance else None
            if not Name: instanceTags['Name'] = f'UNMANAGED { instanceId }'
            if not Owner: instanceTags['Owner'] = tags[dept]['Owner']
            if not Department: instanceTags['Department'] = dept
            logging.info(f'Instance Tags Needed ==> {instanceTags}')
            

            if instanceTags:
                # input("Check tags before proceeding")
                logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging instance { instanceId }...\n")
                AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:instance/{ instanceId }", instanceTags)
            else: logging.info(f"aws_ec2_tag_all_resources.py ==> Instance { instanceId } already tagged properly. Skipping...")

            # TAG AMIs OF INSTANCE
            instanceName = Name[0] if Name else f'UNMANAGED { instanceId }'
            instanceAMIs = [ ami for ami in images if instance['ImageId'] == ami['ImageId'] ]
            
            if instanceAMIs:
                logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging AMI associated with { instanceName }")

                for ami in instanceAMIs:    
                    logging.info(f"Current AMI Tags ==> { ami['Tags'] }")
                    amiTags = {}
                    ami_Name = [ tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in ami else None
                    ami_Owner = [ tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in ami else None
                    ami_Department = [ tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in ami else None   
                    if not ami_Name: amiTags['Name'] = f"{ ami['Name'] }"
                    if not ami_Owner: amiTags['Owner'] = tags[dept]['Owner']
                    if not ami_Department: amiTags['Department'] = dept     
                    logging.info(f'AMI Tags Needed ==> { amiTags }')
                        
                    if amiTags: 
                        # input("Check tags before proceeding")
                        logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging AMI { ami['ImageId'] }...")
                        AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:image/{ ami['ImageId'] }", amiTags)
                    else: logging.info(f"aws_ec2_tag_all_resources.py ==> AMI { ami['ImageId'] } already tagged properly. Skipping...")
            else: logging.info(f"aws_ec2_tag_all_resources.py ==> No AMIs associated with { instanceName }. Skipping...")

            # TAG ATTACHED VOLUMES
            volumeIds = [ vol['Ebs']['VolumeId'] for vol in instance['BlockDeviceMappings'] if 'Ebs' in vol ]
            volumes = AWS.getVolumes(volumeIds) if volumeIds else None
            if volumes: 
                logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging volumes attached to { instanceName } ==> { volumeIds }")
                for vol in volumes: 
                    logging.info(f"Current Volume Tags ==> { vol['Tags'] if 'Tags' in vol else {} }")
                    volumeTags = {}
                    vol_Name = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in vol else None
                    vol_Owner = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in vol else None
                    vol_Department = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in vol else None 
                    if not vol_Name or vol_Name == 'executor-prod/executor-prod-executor/compute-nodes-xlarge-us-east-1b-volume--i-038c562e97cede9ca': volumeTags['Name'] = f"{instanceName}-volume--{instanceId}"
                    if not vol_Owner or vol_Name == 'executor-prod/executor-prod-executor/compute-nodes-xlarge-us-east-1b-volume--i-038c562e97cede9ca': volumeTags['Owner'] = tags[dept]['Owner']
                    if not vol_Department or vol_Name == 'executor-prod/executor-prod-executor/compute-nodes-xlarge-us-east-1b-volume--i-038c562e97cede9ca': volumeTags['Department'] = dept          

                    logging.info(f'Volume Tags Needed ==> {volumeTags}')
                    

                    if volumeTags:
                        # input("Check tags before proceeding")
                        logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging volume { vol['VolumeId'] }...")
                        AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:volume/{ vol['VolumeId'] }", volumeTags)
                    else: logging.info(f"aws_ec2_tag_all_resources.py ==> Volume { vol['VolumeId'] } already tagged properly. Skipping...")
            else: logging.info(f"aws_ec2_tag_all_resources.py ==> No volumes attached to { instanceName }. Skipping...")

            # TAG SNAPSHOTS OF VOLUME
                    # snapshots = AWS.getEc2Snapshots(ec2)
                    # [ AWS.tagResource(snapshot, tags[dept]) for snapshot in snapshots if snapshots ]

            # TAG ATTACHED NETWORK INTERFACES
            interfaceIds = [ eni['NetworkInterfaceId'] for eni in instance['NetworkInterfaces'] ]
            interfaces = AWS.getNetworkInterfaces(interfaceIds) if interfaceIds else None
            if interfaces: 
                logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging network interfaces attached to {instanceName} ==> {interfaceIds}")
                for eni in interfaces: 
                    logging.info(f"Current Network Interface Tags ==> {eni['TagSet']}")
                    eniTags = {}
                    eni_Name = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Name' ] if 'TagSet' in eni else None
                    eni_Owner = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Owner' ] if 'TagSet' in eni else None
                    eni_Department = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Department' ] if 'TagSet' in eni else None 
                    if not eni_Name or eni_Name == 'executor-prod/executor-prod-executor/compute-nodes-xlarge-us-east-1b-eni--i-038c562e97cede9ca': eniTags['Name'] = f"{instanceName}-eni--{instanceId}"
                    if not eni_Owner or eni_Name == 'executor-prod/executor-prod-executor/compute-nodes-xlarge-us-east-1b-eni--i-038c562e97cede9ca': eniTags['Owner'] = tags[dept]['Owner']
                    if not eni_Department or eni_Name == 'executor-prod/executor-prod-executor/compute-nodes-xlarge-us-east-1b-eni--i-038c562e97cede9ca': eniTags['Department'] = dept  

                    logging.info(f'Network Interface Tags ==> { eniTags }')
                    
                    if eniTags:
                        # input("Check tags before proceeding")
                        logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging network interface { eni['NetworkInterfaceId'] }...")
                        AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:network-interface/{ eni['NetworkInterfaceId'] }", eniTags)
                    else: logging.info(f"aws_ec2_tag_all_resources.py ==> Network Interface { eni['NetworkInterfaceId'] } already tagged properly. Skipping...")

            # TAG ELASTIC IPs ATTACHED TO NETWORK INTERFACE
                    EIP = instance['NetworkInterfaces']['Association']['AllocationId'] if 'Association' in instance['NetworkInterfaces'] else None
                    if EIP:
                        logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging Elastic IP associated with interface { eni['NetworkInterfaceId'] } on { instanceName } ==> { instanceAMIs }")
                        eipTags = {}
                        eipTags['Name'] = f"{instanceName}-eip--{instanceId}"
                        eipTags['Owner'] = tags[dept]['Owner']
                        eipTags['Department'] = dept 
                        input("Check tags before proceeding")

                        logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging elastic IP { EIP }...")
                        AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:eip/{ EIP }", tags[dept])
            else: logging.info(f"aws_ec2_tag_all_resources.py ==> No network interfaces attached to { instanceName }. Skipping...")

            logging.info(f'aws_ec2_tag_all_resources.py ==> Completed tagging for instance: { instanceName }\n\n')
    logging.info(f'aws_ec2_tag_all_resources.py ==> Completed tagging for { dept } department\n\n')
logging.info(f'aws_ec2_tag_all_resources.py ==> Completed ALL tagging. Quitting.')

