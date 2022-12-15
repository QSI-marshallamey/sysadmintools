import json
import re
from AWS import AWS as aws

def lambda_handler(event, context):
    AWS = aws()
    instanceId = event['detail']['instance-id']
    instance = AWS.getInstance(instanceId)

    ## TAG INSTANCE
    print(f'aws_ec2_tag_all_resources.py ==> Tagging { instanceId }...')
    print(f"Current Tags ==> { instance['Tags'] }")
    instanceTags = {}
    Name = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in instance else None
    Owner = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in instance else None
    Department = [ tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in instance else None
    
    if Name and (bool(re.match(r"Compute", Name[0])) or  bool(re.match(r"holocron-spark*", Name[0]))): 
        if not Owner: instanceTags['Owner'] = "galppay@quantum-si.com"
        if not Department: instanceTags['Department'] = "rnd"
    elif Name and (bool(re.match(r"bespin-*", Name[0])) or  bool(re.match(r"executor-*", Name[0]))):
        if not Owner: instanceTags['Owner'] = "sliu@quantum-si.com"
        if not Department: instanceTags['Department'] = "cloud"
    elif not Name: instanceTags['Name'] = f'UNMANAGED { instanceId }'
    instanceName = Name[0] if Name else f'UNMANAGED { instanceId }'
    print(f'Instance Tags Needed ==> {instanceTags}')
    
    if instanceTags:
        print(f"aws_ec2_tag_all_resources.py ==> Tagging instance { instanceId }...\n")
        AWS.tagResource(f"arn:aws:ec2:us-east-1:{ event['account'] }:instance/{ instanceId }", instanceTags)
    else: print(f"aws_ec2_tag_all_resources.py ==> Instance { instanceId } already tagged properly. Skipping...")

    
    # TAG ATTACHED VOLUMES
    volumeIds = [ vol['Ebs']['VolumeId'] for vol in instance['BlockDeviceMappings'] if 'Ebs' in vol ]
    volumes = AWS.getVolumes(volumeIds) if volumeIds else None
    if volumes: 
        print(f"aws_ec2_tag_all_resources.py ==> Tagging volumes attached to { instanceName } ==> { volumeIds }")
        for vol in volumes: 
            print(f"Current Volume Tags ==> { vol['Tags'] if 'Tags' in vol else {} }")
            volumeTags = {}
            vol_Name = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Name' ] if 'Tags' in vol else None
            vol_Owner = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Owner' ] if 'Tags' in vol else None
            vol_Department = [ tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'Department' ] if 'Tags' in vol else None 
            if not vol_Name: volumeTags['Name'] = f"{instanceName}-volume--{instanceId}"
            if not vol_Owner: volumeTags['Owner'] = instanceTags['Owner']
            if not vol_Department: volumeTags['Department'] = instanceTags['Department']          

            print(f'Volume Tags Needed ==> {volumeTags}')
            if volumeTags:
                print(f"aws_ec2_tag_all_resources.py ==> Tagging volume { vol['VolumeId'] }...")
                AWS.tagResource(f"arn:aws:ec2:us-east-1:{ event['account'] }:volume/{ vol['VolumeId'] }", volumeTags)
            else: print(f"aws_ec2_tag_all_resources.py ==> Volume { vol['VolumeId'] } already tagged properly. Skipping...")
    else: print(f"aws_ec2_tag_all_resources.py ==> No volumes attached to { instanceName }. Skipping...")

    # TAG SNAPSHOTS OF VOLUME
            # snapshots = AWS.getEc2Snapshots(ec2)
            # [ AWS.tagResource(snapshot, tags[dept]) for snapshot in snapshots if snapshots ]

    # TAG ATTACHED NETWORK INTERFACES
    interfaceIds = [ eni['NetworkInterfaceId'] for eni in instance['NetworkInterfaces'] ]
    interfaces = AWS.getNetworkInterfaces(interfaceIds) if interfaceIds else None
    if interfaces: 
        print(f"aws_ec2_tag_all_resources.py ==> Tagging network interfaces attached to {instanceName} ==> {interfaceIds}")
        for eni in interfaces: 
            print(f"Current Network Interface Tags ==> {eni['TagSet']}")
            eniTags = {}
            eni_Name = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Name' ] if 'TagSet' in eni else None
            eni_Owner = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Owner' ] if 'TagSet' in eni else None
            eni_Department = [ tag['Value'] for tag in eni['TagSet'] if tag['Key'] == 'Department' ] if 'TagSet' in eni else None 
            if not eni_Name: eniTags['Name'] = f"{instanceName}-eni--{instanceId}"
            if not eni_Owner: eniTags['Owner'] = instanceTags['Owner']
            if not eni_Department: eniTags['Department'] = instanceTags['Department']  

            print(f'Network Interface Tags ==> { eniTags }')
            if eniTags:
                print(f"aws_ec2_tag_all_resources.py ==> Tagging network interface { eni['NetworkInterfaceId'] }...")
                AWS.tagResource(f"arn:aws:ec2:us-east-1:{ event['account'] }:network-interface/{ eni['NetworkInterfaceId'] }", eniTags)
            else: print(f"aws_ec2_tag_all_resources.py ==> Network Interface { eni['NetworkInterfaceId'] } already tagged properly. Skipping...")

    # TAG ELASTIC IPs ATTACHED TO NETWORK INTERFACE
            EIP = instance['NetworkInterfaces']['Association']['AllocationId'] if 'Association' in instance['NetworkInterfaces'] else None
            if EIP:
                print(f"aws_ec2_tag_all_resources.py ==> Tagging Elastic IP associated with interface { eni['NetworkInterfaceId'] } on { instanceName } ==> { instanceAMIs }")
                eipTags = {}
                eipTags['Name'] = f"{instanceName}-eip--{instanceId}"
                eipTags['Owner'] = instanceTags['Owner']
                eipTags['Department'] = instanceTags['Department'] 

                print(f"aws_ec2_tag_all_resources.py ==> Tagging elastic IP { EIP }...")
                AWS.tagResource(f"arn:aws:ec2:us-east-1:{ event['account'] }:eip/{ EIP }", tags[dept])
    else: print(f"aws_ec2_tag_all_resources.py ==> No network interfaces attached to { instanceName }. Skipping...")
    print(f'aws_ec2_tag_all_resources.py ==> Completed tagging for instance: { instanceName }\n\n')

    return {
    'statusCode': 200,
    'body': json.dumps(f'Completed tagging for instance { instanceId }: { instanceName }')
    }
