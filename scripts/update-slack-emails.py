#!/usr/bin/env python3
import sys
import argparse

sys.path.insert(1, '/Users/marshallamey/bin/sysadmintools/lib')
from Authentication import Authentication
from Staff import Staff 

#1 Parse command arguments
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keys', 
    help='provide path to admin keys', 
    default='../ADMIN_KEYS.py', 
    metavar=''
)
args = parser.parse_args()

#2 Create necessary variables
auth = Authentication(args.keys) if args.keys else Authentication() 
staff = Staff('', auth)

#3 Create list of Slack users
slackUsers = staff.getAllSlackUsers()
for user in slackUsers: 
    if 'email' in user['profile']: print(user['profile']['email'])
#4 Update emails in list
# for user in slackUsers:
#     try:
#         if '@detectnow.com' in user['profile']['email']:
#             print(f"Updating {user['profile']['email']}") 
#             staff.updateSlackEmail(user)
#     except:
#         print(f"{user['name']} has no email")