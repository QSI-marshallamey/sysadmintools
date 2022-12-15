from botocore.exceptions import ClientError
import boto3

class AWS:
    '''
    A class for performing common tasks in AWS.
    '''
    def __init__(self):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.ec2_client = boto3.client('ec2')
        self.rg_client = boto3.client('resource-groups')

##################################################################################################
####################################  {{       EC2       }}  #####################################
##################################################################################################
    def getInstance(self, id):
        try: 
            response = self.ec2_client.describe_instances( InstanceIds=[id] )

            if response['Reservations']: return response['Reservations'][0]['Instances'][0]
            else: 
                print(f'ERROR: Instance may no longer exist. {response}')
                return False
        except ClientError as e:
            print(f'ERROR: {e}')
            return False

    def getImages(self):
        try: 
            response = self.ec2_client.describe_images(Owners=['300212233050'])
            if 'ResponseMetadata' in response: return response['Images']
            else: 
                print(f'ERROR: {response}')
                return False
        except ClientError as e:
            print(f'ERROR: {e}')
            return False

    def getVolumes(self, ids):
        try: 
            response = self.ec2_client.describe_volumes(VolumeIds=ids)
            if 'ResponseMetadata' in response: return response['Volumes']
            else: 
                print(f'ERROR: {response}')
                return False
        except ClientError as e:
            print(f'ERROR: {e}')
            return False

    def getNetworkInterfaces(self, ids):
        try: 
            response = self.ec2_client.describe_network_interfaces(NetworkInterfaceIds=ids)
            if 'ResponseMetadata' in response: return response['NetworkInterfaces']
            else: 
                print(f'ERROR: {response}')
                return False
        except ClientError as e:
            print(f'ERROR: {e}')
            return False


#### TAG RESOURCES
    def tagResource(self, resource, tags):
        tagger = boto3.client('resourcegroupstaggingapi')
        try: 
            response = tagger.tag_resources(
                ResourceARNList=[ resource ],
                Tags=tags
            )
            if 'ResponseMetadata' in response: return response
            else: 
                print(f'ERROR: {response}')
                return False
        except ClientError as e:
            print(f'ERROR: {e}')
            return False
