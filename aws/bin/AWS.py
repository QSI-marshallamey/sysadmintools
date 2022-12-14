from urllib import response
import json
from botocore.exceptions import ClientError
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
        self.session = boto3.Session(profile_name=profile)
        self.cf_client = boto3.client('cloudformation')
        self.ssm_client = boto3.client('ssm')
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.ec2_resource = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')
        self.ecr_client = boto3.client('ecr')
        self.sqs_client = boto3.client('sqs')
        self.rg_client = boto3.client('resource-groups')

##################################################################################################
#####################################  {{ CLOUDFORMATION }}  #####################################
##################################################################################################
    def getStacks(self, stack_names=None):
        try: response = self.cf_client.describe_stacks(stack_names) if stack_names else self.cf_client.describe_stacks()
        except ClientError as e:
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
        except ClientError as e:
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
        except ClientError as e:
            logging.error(e)
            return False
        return self.getBucket(bucket_name)

    def getBucket(self, name):
        return self.s3_resource.Bucket(name)

    def listBuckets(self):  
        '''
        DEFINITION: This is a definition
        '''
        S3 = self.session.client('s3')
        try:
            response = S3.list_buckets()
            if 'Buckets' in response: return response['Buckets']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
        
    def deleteBucket(self, bucket):
        try: return bucket.delete()
        except: return False
    
    def getBucketPolicy(self, bucket):
        S3 = self.session.client('s3')
        try:
            response = S3.get_bucket_policy( Bucket=bucket )
            if 'Policy' in response: return response['Policy']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False          

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
        except ClientError as e:
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
        except ClientError as e:
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
        except ClientError as e:
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
        except ClientError as e:
            logging.error(e)
            return False

    def getBucketEncryptionPolicy(self, bucket):
        try:
            response = self.s3_client.get_bucket_encryption(
                Bucket=bucket
            )
            if 'ServerSideEncryptionConfiguration' in response: return response
            elif 'ServerSideEncryptionConfigurationNotFoundError' in response:
                logging.info(f'INFO: No encryption configuration for this bucket')
                return False
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
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
            if 'ResponseMetadata' in response: return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def requireSSL(self, bucket, updatedPolicy):
        S3 = self.session.client('s3')
        try:
            response = S3.put_bucket_policy(
                Bucket=bucket,
                Policy=updatedPolicy
            )
            if 'ResponseMetadata' in response: return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
    
    def getBucketLoggingStatus(self, bucket):
        try:
            response = self.s3_client.get_bucket_logging( Bucket=bucket )
            if 'LoggingEnabled' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def enableBucketLogging(self, bucket, targetBucket, targetPrefix=f's3-access-logs'):
        # DEFINITION: This is a definition
        try:
            response = self.s3_client.put_bucket_logging(
                Bucket=bucket,
                BucketLoggingStatus={
                    'LoggingEnabled': {
                        'TargetBucket': targetBucket,
                        'TargetPrefix': f's3-access-logs/{bucket}/'
                    }
                }
            )
            if 'ResponseMetadata' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def getLifecyclePolicy(self, bucket):
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration( Bucket=bucket )
            if 'Rules' in response: return response
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
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
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

##################################################################################################
##########################################  {{ SNS }}  ###########################################
##################################################################################################
    def listTopics(self):  
        try:
            SNS = self.session.client('sns')
            allTopics = []
            response = SNS.list_topics()
            
            if 'Topics' in response: 
                allTopics.extend(response['Topics'])
                while 'NextToken' in response:
                    response = SNS.list_topics(NextToken=response['NextToken'])
                    allTopics.extend(response['Topics'])
                return allTopics
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
    
    def getTopicAttributes(self, TopicArn):
        try:
            SNS = self.session.client('sns')
            response = SNS.get_topic_attributes( TopicArn=TopicArn )
            if 'Attributes' in response: return response['Attributes']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def enableTopicEncryption(self, TopicArn, KeyId='alias/aws/sns'):
        try:
            SNS = self.session.client('sns')
            response = SNS.set_topic_attributes(
                TopicArn=TopicArn,
                AttributeName='KmsMasterKeyId',
                AttributeValue=KeyId
            )
            if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200: 
                return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def enableTopicLogging(self, TopicArn):
        try:
            SNS = self.session.client('sns')
            accountId = self.session.client('sts').get_caller_identity()['Account']
            response = SNS.set_topic_attributes(
                TopicArn=TopicArn,
                AttributeName='HTTPFailureFeedbackRoleArn',
                AttributeValue=f'arn:aws:iam::{accountId}:role/SNSFailureFeedback'
            )
            response = SNS.set_topic_attributes(
                TopicArn=TopicArn,
                AttributeName='HTTPSuccessFeedbackRoleArn',
                AttributeValue=f'arn:aws:iam::{accountId}:role/SNSSuccessFeedback'
            )
            response = SNS.set_topic_attributes(
                TopicArn=TopicArn,
                AttributeName='HTTPSuccessFeedbackSampleRate',
                AttributeValue='0'
            )
            if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200: 
                return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

##################################################################################################
##########################################  {{ SQS }}  ###########################################
##################################################################################################

    def listQueues(self):  
        try:
            response = self.sqs_client.list_queues()
            if 'QueueUrls' in response: return response['QueueUrls']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False
    
    def getQueueAttributes(self, queueUrl):
        try:
            response = self.sqs_client.get_queue_attributes(
                QueueUrl=queueUrl,
                AttributeNames=['KmsMasterKeyId','KmsDataKeyReusePeriodSeconds','SqsManagedSseEnabled']
            )
            if 'Attributes' in response: return response['Attributes']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def enableQueueEncryption(self, queueUrl, attributes):
        try:
            response = self.sqs_client.set_queue_attributes(
                QueueUrl=queueUrl,
                Attributes=attributes
            )
            if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200: 
                return True
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
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
        except ClientError as e:
            logging.error(e)
            return False
        return response

    def getEnvVariable(self, name):
        try: response = self.ssm_client.get_parameter(Name=name, WithDecryption=True)
        except ClientError as e:
            logging.error(e)
            return False
        return response['Parameter']['Value']
    
    def deleteEnvVariable(self, name):
        try: response = self.ssm_client.delete_parameter(Name=name)
        except ClientError as e:
            logging.error(e)
            return False
        return print(f"{name} deleted.")


##################################################################################################
####################################  {{       EC2       }}  #####################################
##################################################################################################
    def getSecurityGroups(self):
        try: response = self.ec2_client.describe_security_groups()
        except ClientError as e:
            logging.error(e)
            return False
        logging.info(response)
        return response
    
    def getEc2Resources(self, dept):
        departments = {
            'chips': 'chips-ec2-resources',
            'cloud': 'cloud-ec2-resources',
            'it': 'it-ec2-resources',
            'rnd': 'rnd-ec2-resources'
        }
        try: 
            response = self.rg_client.list_group_resources(
            Group=departments[dept],
            Filters=[{
                'Name': 'resource-type',
                'Values': [ 'AWS::EC2::Instance']
            }]
        )
            if 'ResponseMetadata' in response: return response['Resources']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def getInstance(self, id):
        try: 
            response = self.ec2_client.describe_instances( InstanceIds=[id] )

            if response['Reservations']: return response['Reservations'][0]['Instances'][0]
            else: 
                logging.error(f'ERROR: Instance may no longer exist. {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def getImages(self):
        try: 
            response = self.ec2_client.describe_images(Owners=['300212233050'])
            if 'ResponseMetadata' in response: return response['Images']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def getVolumes(self, ids):
        try: 
            response = self.ec2_client.describe_volumes(VolumeIds=ids)
            if 'ResponseMetadata' in response: return response['Volumes']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

    def getNetworkInterfaces(self, ids):
        try: 
            response = self.ec2_client.describe_network_interfaces(NetworkInterfaceIds=ids)
            if 'ResponseMetadata' in response: return response['NetworkInterfaces']
            else: 
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False

##################################################################################################
###############################  {{ ELASTIC CONTAINER REGISTRY }}  ###############################
##################################################################################################
    def getRepos(self):
        try: response = self.ecr_client.describe_repositories()
        except ClientError as e:
            logging.error(e)
            return False
        return response['repositories']

    def enableImageScanning(self, repo, accountId):
        try: response = self.ecr_client.put_image_scanning_configuration(
            registryId=accountId,
            repositoryName=repo,
            imageScanningConfiguration={ 'scanOnPush': True }
        )
        except ClientError as e:
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
        except ClientError as e:
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
        except ClientError as e:
            logging.error(e)
            return False
        logging.info(pformat(response))
        return response

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
                logging.error(f'ERROR: {response}')
                return False
        except ClientError as e:
            logging.error(f'ERROR: {e}')
            return False


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