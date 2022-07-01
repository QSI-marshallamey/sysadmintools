import boto3
import logging
from botocore.exceptions import ClientError

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
        self.ssm_client = boto3.client('ssm')
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')

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

    def listBuckets(self):  
        for bucket in self.s3_resource.buckets.all(): print(bucket.name)

    def getBucket(self, name):
        return self.s3_resource.Bucket(name)
        
    def deleteBucket(self, bucket):
        try: return bucket.delete()
        except: return False
    
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