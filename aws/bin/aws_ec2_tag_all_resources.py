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


### MAIN FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AWS = AWS()
# Get a list of all departments
#departments = ['chips', 'cloud', 'it', 'rnd']
departments = ['rnd']
tags = {
            'chips': { 'Owner': 'jclark@quantum-si.com'  },
            'cloud': { 'Owner': 'sliu@quantum-si.com'    },
            'it':    { 'Owner': 'mamey@quantum-si.com'   },
            'rnd':   { 'Owner': 'galppay@quantum-si.com' }
        }

# Get a list of all AMIs
images = AWS.getImages()
logging.debug(f'getImages() ==> { images }')
logging.info(f'getImages() ==> Found {len(images)} images')

# Get a list of all resources in each department's EC2 resource group
for dept in departments: 
    logging.info(f'aws_ec2_tag_all_resources.py ==> Tagging resources for {dept}')

    instances = AWS.getEc2Resources(dept)
    
    logging.debug(f'getEc2Resources() ==> {instances}')
    logging.info(f'getEc2Resources() ==> Found {len(instances)} {dept} instances\n')

    for i in instances:
        instanceArn = i['Identifier']['ResourceArn']
        instanceId = instanceArn.split('/')[1]
        print(instanceId)
        instance = AWS.getInstance(instanceId)
        if not instance: 
            logging.warning(f'getInstance ==> Instance { instanceId } not found. Skipping \n')
            continue

        ## TAG INSTANCE 
        logging.info(f'getInstance ==> Tagging { instanceArn }...')
        logging.info(f"Current Tags ==> { instance['Tags'] }")

        instanceTags = {}
        Name = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in instance else None
        Owner = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in instance else None
        Department = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in instance else None
        if not Name: instanceTags['Name'] = f'UNMANAGED { instanceId }'
        if not Owner: instanceTags['Owner'] = tags[dept]['Owner']
        if not Department: instanceTags['Department'] = dept

        logging.info(f'New Tags ==> {instanceTags}')
        # input("Check tags before proceeding")

        if instanceTags:
            logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging instance { instanceId }...\n")
            AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:instance/{ instanceId }", instanceTags)
        else: logging.info(f"aws_ec2_tag_all_resources.py ==> Instance { instanceId } already tagged properly. Skipping...\n")

        # TAG AMIs OF INSTANCE
        instanceName = Name[0] if Name else f'UNMANAGED { instanceId }'
        instanceAMIs = [ ami for ami in images if instance['ImageId'] == ami['ImageId'] ]
        logging.info(f"Found AMIs associated with { instanceName } ==> { instanceAMIs }")

        for ami in instanceAMIs:          
            amiTags = {}
            ami_Name = [ tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in ami else None
            ami_Owner = [ tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in ami else None
            ami_Department = [ tag['Value'] for tag in ami['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in ami else None   
            if not ami_Name: amiTags['Name'] = f"{ ami['Name'] }"
            if not ami_Owner: amiTags['Owner'] = tags[dept]['Owner']
            if not ami_Department: amiTags['Department'] = dept     

            logging.info(f'AMI Tags ==> {amiTags}')
            # input("Check tags before proceeding")
            
            if amiTags: 
                logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging image { ami['ImageId'] }...\n")
                AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:image/{ ami['ImageId'] }", amiTags)
            else: logging.info(f"aws_ec2_tag_all_resources.py ==> Image { ami['ImageId'] } already tagged properly. Skipping...\n")

        # TAG ATTACHED VOLUMES
        volumeIds = [ vol['Ebs']['VolumeId'] for vol in instance['BlockDeviceMappings'] if 'Ebs' in vol ]
        volumes = AWS.getVolumes(volumeIds)
        if volumes: 
            logging.info(f"Found volumes attached to { instanceName } ==> { volumes }")
            for vol in volumes: 
                volumeTags = {}
                vol_Name = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in vol else None
                vol_Owner = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in vol else None
                vol_Department = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in vol else None 
                if not vol_Name: volumeTags['Name'] = f"{instanceName}-volume--{instanceId}"
                if not vol_Owner: volumeTags['Owner'] = tags[dept]['Owner']
                if not vol_Department: volumeTags['Department'] = dept          

                logging.info(f'Volume Tags ==> {volumeTags}')
                # input("Check tags before proceeding")

                if volumeTags:
                    logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging volume { vol['VolumeId'] }...\n")
                    AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:volume/{ vol['VolumeId'] }", volumeTags)
                else: logging.info(f"aws_ec2_tag_all_resources.py ==> Volume { vol['VolumeId'] } already tagged properly. Skipping...\n")

        # TAG SNAPSHOTS OF VOLUME
                # snapshots = AWS.getEc2Snapshots(ec2)
                # [ AWS.tagResource(snapshot, tags[dept]) for snapshot in snapshots if snapshots ]

        # TAG ATTACHED NETWORK INTERFACES
        interfaceIds = [ eni['NetworkInterfaceId'] for eni in instance['NetworkInterfaces'] ]
        interfaces = AWS.getNetworkInterfaces(interfaceIds)
        if interfaces: 
            logging.info(f"Found network interfaces attached to {instanceName} ==> {interfaceIds}")
            for eni in interfaces: 
                eniTags = {}
                eni_Name = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Name' ] if 'TagSet' in eni else None
                eni_Owner = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Owner' ] if 'TagSet' in eni else None
                eni_Department = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Department' ] if 'TagSet' in eni else None 
                if not eni_Name: eniTags['Name'] = f"{instanceName}-eni--{instanceId}"
                if not eni_Owner: eniTags['Owner'] = tags[dept]['Owner']
                if not eni_Department: eniTags['Department'] = dept  

                logging.info(f'Network Interface Tags ==> {eniTags}')
                # input("Check tags before proceeding")
                if eniTags:
                    logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging network interface { eni['NetworkInterfaceId'] }...\n")
                    AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:network-interface/{ eni['NetworkInterfaceId'] }", eniTags)
                else: logging.info(f"aws_ec2_tag_all_resources.py ==> Network Interface { eni['NetworkInterfaceId'] } already tagged properly. Skipping...\n")

        # TAG ELASTIC IPs ATTACHED TO NETWORK INTERFACE
                EIP = instance['NetworkInterfaces']['Association']['AllocationId'] if 'Association' in instance['NetworkInterfaces'] else None
                if EIP:
                    logging.info(f"Found Elastic IP associated with interface { eni['NetworkInterfaceId'] } on { instanceName } ==> { instanceAMIs }")
                    eipTags = {}
                    eipTags['Name'] = f"{instanceName}-eip--{instanceId}"
                    eipTags['Owner'] = tags[dept]['Owner']
                    eipTags['Department'] = dept 
                    # input("Check tags before proceeding")

                    logging.info(f"aws_ec2_tag_all_resources.py ==> Tagging elastic IP { EIP }...\n")
                    AWS.tagResource(f"arn:aws:ec2:us-east-1:300212233050:eip/{ EIP }", tags[dept])

        logging.info(f'Completed tagging for instance: { instanceName }\n\n')
    logging.info(f'Completed tagging for { dept } department\n\n')
logging.info(f'Completed ALL tagging. Quitting.')

