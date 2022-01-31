import asyncio
from okta.client import Client as OktaClient
from okta.models import User
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
        self.user = User()

    # def addUser(self):

    async def getUser(self, login):
        user, resp, err = await self.client.get_user(login)
        if err: print("ERROR! User not found in Okta! ==> " + err.message)
        else: return user

    async def getUsers(self, params={}):
        users, resp, err = await self.client.list_users(params)
        if err: print("ERROR! ==> " + str(err))
        else:
            for user in users:
                print(user.profile.first_name, user.profile.last_name)
            print(f'Success! {len(users)} Okta users retrieved in this domain')
            return users

    async def updateUser(self, userID, userProfile):
        updatedUser, res, err = await self.client.partial_update_user(userID, userProfile)
        if err: print("ERROR! ==> " + str(err))
        else: return updatedUser
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