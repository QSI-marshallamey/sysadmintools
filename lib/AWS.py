import boto3

class AWS:
    '''
    A class for performing user related tasks. A path to an excel file containing
    a list of users is required (usersFilePath), as well as an instance of
    the Authentication class to generate the necessary keys (auth)

    VARIABLES
        users: A Python list containing employees as Python dictionaries
        auth: An Authentication object passed during Employee instance creation
    '''
    def __init__(self, domain='4catalyzer.com'):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.domain = domain
        self.s3 = boto3.resource('s3')
        self.ssm = boto3.client('ssm')

    # def createBucket(self):
    def listBuckets(self):
        for bucket in self.s3.buckets.all(): print(bucket.name)
    # def getBucket(self):
    # def deleteBucket(self):
    
    # def createObject(self):
    # def listObjects(self):
    # def getObject(self):
    # def deleteObject(self):
    
    def setEnvVariable(self, name, value, desc, type='SecureString', overwrite=False):
        response = self.ssm.put_parameter(
            Name=name,
            Value=value,
            Type=type,
            Description=desc,
            Overwrite=overwrite
        )
        return response

    def getEnvVariable(self, name):
        response = self.ssm.get_parameter(
            Name=name,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    
    def deleteEnvVariable(self, name):
        return self.ssm.delete_parameter(Name=name)




if __name__ == '__main__':
    A = AWS()
    A.listBuckets()
    A.setEnvVariable('/TestVars/Test1', 'testingtesting123', 'This is a test var')
    print(A.getEnvVariable('/TestVars/Test1')['Parameter']['Value'])