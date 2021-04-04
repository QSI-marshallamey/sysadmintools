'''
This file is required to perform any functions that require user authentication such as 
signing in to accounts and acquiring access tokens

OPTION 1: Copy to secure location, enter data, and rename, if desired. Input file path when prompted.
OPTION 2: (not recommended) Enter data and leave file in the working directory. Be sure to comment 
out the removeKeys function from any script you use or else your key file will be deleted.
'''

adminPhone = '<<Enter information>>'
adminEmail = '<<Enter information>>'
gitToken = '<<Enter information>>'
keys = {
    'DEFAULT_PASSWORD': '<<For creating new accounts>>',
    'REDIRECT_URI': '<<Enter information>>',
    'google': {
        'EMAIL': '<<Enter information>>',
        'PASSWORD': '<<Enter information>>',
        'CLIENT_ID':'<<Enter information>>',
        'CLIENT_SECRET': '<<Enter information>>',
        'API_KEY': '<<Enter information>>',
        'AUTH_CODE': '<<PROVIDED BY GOOGLE>>',
        'ACCESS_TOKEN': '<<PROVIDED GOOGLE>>',
        'STATE': '<<Enter information>>'
    },
    'slack': {
        'ACCESS_TOKEN': '<<Enter information>>'
    },
    'harvest': {
        'ACCESS_TOKEN': '<<Enter information>>'
    },
    'zoom': {
        'ACCESS_TOKEN': '<<Enter information>>'
    },
    'twilio': {
        'accountSID': '<<Enter information>>',
        'authToken': '<<Enter information>>' ,
    }
}


