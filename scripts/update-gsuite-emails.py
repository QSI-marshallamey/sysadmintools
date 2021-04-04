#!/usr/bin/env python3
import sys
import argparse

sys.path.insert(1, '/Users/marshallamey/bin/sysadmintools/lib')
from Authentication import Authentication
from Staff import Staff 

parser = argparse.ArgumentParser()
parser.add_argument( '-k', '--keys', 
    help='provide path to admin keys', 
    default='../ADMIN_KEYS.py', 
    metavar=''
)
args = parser.parse_args()
auth = Authentication(args.keys) if args.keys else Authentication()


OLD_DOMAIN = 'detectnow.com'
NEW_DOMAIN = 'detect.com'

staff = Staff('', auth)
allUsers = staff.getAllGSuiteUsers()
# print(allUsers)
# print(len(allUsers))

#allUsers = ['test@detectnow.com', 'jkottage@detectnow.com', 'pproto@detectnow.com']


for user in allUsers: staff.updateGSuiteEmail(user, user.replace(OLD_DOMAIN, NEW_DOMAIN))

# COMMENT OUT TO STOP REMOVAL OF ADMIN KEYS AFTER SCRIPT EXIT (not recommended)
#if staff.auth.removeKeys(): print('Keys safely removed from working directory')
#else: print('Keys not removed from working directory.')
