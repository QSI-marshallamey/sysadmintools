import asyncio
from okta.client import Client as OktaClient
from AWS import AWS

class Okta:
    '''
    A class for performing user related tasks. A path to an excel file containing
    a list of users is required (usersFilePath), as well as an instance of
    the Authentication class to generate the necessary keys (auth)

    VARIABLES
        users: A Python list containing employees as Python dictionaries
        auth: An Authentication object passed during Employee instance creation
    '''

    def __init__(self, domain):
        # Save keys in file keys object
        #For every user, format data and add to user list
        self.domain = domain
        A = AWS()
        API_TOKEN = A.getEnvVariable('/'+ domain +'/okta/apiToken')
        config = {
            'orgUrl': f'https://{domain}.okta.com',
            'token': API_TOKEN
        }
        self.client = OktaClient(config)

    # def addUser(self):
    # def getUser(self):
    async def getUsers(self):
        users, resp, err = await self.client.list_users()
        for user in users:
            print(user.profile.first_name, user.profile.last_name)
        print(f'Successfully connected!! {len(users)} Okta users found in this domain')

    # def updateUser(self):
    # def suspendUser(self):
    # def activateUser(self):
    # def unsuspendUser(self):
    # def addUserToGroup(self):
    # def removeUserFromGroup(self):
    
    # Test for connectivity, list all users and print their first name and last name
    async def test(self):
        users, resp, err = await self.client.list_users()
        for user in users:
            print(user.profile.first_name, user.profile.last_name)
        print(f'Successfully connected!! {len(users)} Okta users found in this domain')


if __name__ == '__main__':
    OKTA = Okta('4catalyzer')
    print(f'Testing connection to {OKTA.domain}.okta.com')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(OKTA.test())