from urllib import response
import json
from botocore import exceptions
import botocore
import boto3
import logging
from pprint import pprint, pformat


class AWS:
    '''
    A class for performing common tasks in AWS.

    VARIABLES
        profile: AWS Profile in configs to use for this instance
    '''
    def __init__(self, profile='default'):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.profile = profile
        self.cf_client = boto3.client('cloudformation')
        self.ssm_client = boto3.client('ssm')
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.ec2_client = boto3.client('ec2')
        self.ecr_client = boto3.client('ecr')

##################################################################################################
#####################################  {{ CLOUDFORMATION }}  #####################################
##################################################################################################
    def getStacks(self, stack_names=None):
        try: response = self.cf_client.describe_stacks(stack_names) if stack_names else self.cf_client.describe_stacks()
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        logging.info('This script will attempt to enable notifications on the following stacks:')
        for stack in response['Stacks']: logging.info(stack['StackName'])
        logging.info('')
        return response['Stacks']
    
    def updateNotificationARNs(self, stack, topics):
        updatedParams = stack['Parameters'] if 'Parameters' in stack else []
        for param in updatedParams:
            del param['ParameterValue']
            param['UsePreviousValue'] = True
        print(updatedParams)
        input('Look goood!?')
        try: response = self.cf_client.update_stack(
            StackName=stack['StackName'],
            NotificationARNs=topics,
            UsePreviousTemplate=True,
            Parameters=updatedParams
        )
        except exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InsufficientCapabilitiesException':
                logging.error(f'INSUFFICIENT CAPABILITIES ERROR: {e}')
                input('Try again!?')
                response = self.cf_client.update_stack(
                    StackName=stack['StackName'],
                    NotificationARNs=topics,
                    UsePreviousTemplate=True,
                    Parameters=updatedParams,
                    Capabilities=['CAPABILITY_IAM']
                )
            else:    
                logging.error(f' ERROR: {e}')
                return False
        logging.info(f"SUCCESS: Updated { response['StackId'] }\n")
        return response['StackId']

##################################################################################################
#####################################  {{       S3       }}  #####################################
### https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client ####
##################################################################################################
    def createBucket(self, bucket_name, region=None):
        try:
            if region is None:
                print(f'Creating bucket {bucket_name}')
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                print('Creating bucket in specific region')
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        return self.getBucket(bucket_name)

    def getBucket(self, name):
        return self.s3_resource.Bucket(name)

    def listBuckets(self):  
        try:
            response = self.s3_client.list_buckets()
            if 'Buckets' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
        
    def deleteBucket(self, bucket):
        try: return bucket.delete()
        except: return False
    
    def getBucketPolicy(self, bucket):
        return self.s3_client.get_bucket_policy(Bucket=bucket)

    def enableBucketVersioning(self, bucket):
        try:
            response = self.s3_client.put_bucket_versioning(
                Bucket=bucket,
                VersioningConfiguration={'Status': 'Enabled'}
            )  
            if 'ResponseMetadata' in response: return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def suspendBucketVersioning(self, bucket):
        try:
            response = self.s3_client.put_bucket_versioning(
                Bucket=bucket,
                VersioningConfiguration={'Status': 'Suspended'}
            )  
            if 'ResponseMetadata' in response: return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
        
    def putPublicAccessBlock(self, bucket):
        return self.s3_client.put_public_access_block(
            Bucket=f"{bucket}",
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
    
    def createObject(self, bucket, filepath, key):
        try: bucket.upload_file(filepath, key)
        except: return False
        return True

    def listObjects(self, bucket):
        for object in bucket.objects.all(): print(object)

    def getObject(self, bucket, key):
        try: return bucket.Object(key)
        except: return False

    def deleteObject(self, bucket, key):
        try: bucket.Object(key).delete()
        except: return False
    
    def getEventNotifications(self, bucket):
        try: return self.s3_client.get_bucket_notification_configuration(Bucket=bucket)
        except exceptions.ClientError as e:
            logging.error(e)
            return False

    def setEventNotifications(self, bucket, config):
        try:
            self.s3_client.put_bucket_notification_configuration(
                Bucket=bucket,
                NotificationConfiguration=config,
                SkipDestinationValidation=True
            )
            return True
        except exceptions.ClientError as e:
            logging.error(e)
            return False

    def getBucketEncryptionPolicy(self, bucket):
        try:
            response = self.s3_client.get_bucket_encryption(
                Bucket=bucket
            )
            if 'ServerSideEncryptionConfiguration' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(e)
            return False   

    def enableBucketEncryption(self, bucket):
        try:
            response = self.s3_client.put_bucket_encryption(
                Bucket=bucket,
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': { 'SSEAlgorithm': 'AES256' }
                    }]
                }
            )
            if response is None: return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def requireSSL(self, bucket, updatedPolicy):
        try:
            response = self.s3_client.put_bucket_policy(
                Bucket=bucket,
                Policy=updatedPolicy
            )
            if 'ResponseMetadata' in response: return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
    
    def getBucketLoggingStatus(self, bucket):
        try:
            response = self.s3_client.get_bucket_logging( Bucket=bucket )
            if 'LoggingEnabled' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def enableBucketLogging(self, bucket, targetBucket, targetPrefix=f's3-access-logs/'):
        try:
            response = self.s3_client.put_bucket_logging(
                Bucket=bucket,
                BucketLoggingStatus={
                    'LoggingEnabled': {
                        'TargetBucket': targetBucket,
                        'TargetPrefix': f'{targetPrefix}{bucket}'
                    }
                }
            )
            if 'ResponseMetadata' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def getLifecyclePolicy(self, bucket):
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration( Bucket=bucket )
            if 'Rules' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def setLifecyclePolicy(self, bucket, policy):
        try:
            response = self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket,
                LifecycleConfiguration=policy
            )
            if 'ResponseMetadata' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except exceptions.ClientError as e:
            logging.error(f'ERROR: {e}')
            return False



##################################################################################################
####################################  {{ SYSTEMS MANAGER }}  #####################################
##################################################################################################
    def setEnvVariable(self, name, value, desc, overwrite=False, type='SecureString'):
        try: 
            response = self.ssm_client.put_parameter(
                Name=name,
                Value=value,
                Type=type,
                Description=desc,
                Overwrite=overwrite
            )
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        return response

    def getEnvVariable(self, name):
        try: response = self.ssm_client.get_parameter(Name=name, WithDecryption=True)
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        return response['Parameter']['Value']
    
    def deleteEnvVariable(self, name):
        try: response = self.ssm_client.delete_parameter(Name=name)
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        return print(f"{name} deleted.")


##################################################################################################
####################################  {{       EC2       }}  #####################################
##################################################################################################
    def getSecurityGroups(self):
        try: response = self.ec2_client.describe_security_groups()
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        logging.info(response)
        return response

##################################################################################################
###############################  {{ ELASTIC CONTAINER REGISTRY }}  ###############################
##################################################################################################
    def getRepos(self):
        try: response = self.ecr_client.describe_repositories()
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        logging.info('***** ALL REPOSITORIES *****')
        logging.info(pformat(response['repositories']))
        logging.info('')
        return response['repositories']

    def enableImageScanning(self, repo, accountId):
        try: response = self.ecr_client.put_image_scanning_configuration(
            registryId=accountId,
            repositoryName=repo,
            imageScanningConfiguration={ 'scanOnPush': True }
        )
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        logging.info(pformat(response))
        return response
    
    def enableTagImmutability(self, repo, accountId):
        try: response = self.ecr_client.put_image_tag_mutability(
            registryId=accountId,
            repositoryName=repo,
            imageTagMutability='IMMUTABLE'
        )
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        logging.info(pformat(response))
        return response

    def enableLifecyclePolicy(self, repo, accountId, policy):
        try: response = self.ecr_client.put_lifecycle_policy(
            registryId=accountId,
            repositoryName=repo,
            lifcyclePolicyText=policy
        )
        except exceptions.ClientError as e:
            logging.error(e)
            return False
        logging.info(pformat(response))
        return response

if __name__ == '__main__':
    A = AWS()

    ## S3 BUCKETS AND OBJECTS
    testBucket1 = A.createBucket('marshalls-test-bucket-2345')
    print(f"createBucket():: {testBucket1}")

    testBucket2 = A.getBucket('marshalls-test-bucket-2345')
    print(f"getBucket():: {testBucket2}")
    
    print(f"listBuckets()::")
    A.listBuckets()
    input("Check S3 to verify")
    
    testObject1 = A.createObject(testBucket1, '/Users/marshallamey/bin/helloWorld.py', 'Hello World')
    print(f"createObject():: {testObject1}")  

    testObject2 = A.getObject(testBucket2, 'Hello World')
    print(f"getObject():: {testObject2}")

    print(f"listObjects()::")
    A.listObjects(testBucket2)
    input("Check S3 to verify")

    A.deleteObject(testBucket2, 'Hello World')
    print(f"deleteObject()::Test object deleted.")
    input("Check S3 to verify")

    A.deleteBucket(testBucket2)
    print(f"deleteBucket()::Test bucket deleted.")
    input("Check S3 to verify")

    ## ENVIRONMENT VARIABLES (SSM PARAMETERS)
    A.setEnvVariable('/TestVars/Test1', 'testingtesting123', 'This is a test var', True)
    print(A.getEnvVariable('/TestVars/Test1'))
    A.deleteEnvVariable('/TestVars/Test1')