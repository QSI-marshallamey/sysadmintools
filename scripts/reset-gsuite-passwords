#!/usr/bin/env python3

import argparse
import json
from datetime import datetime

sys.path.insert(1, '/Users/marshallamey/bin/sysadmintools/lib')
from Authentication import Authentication
from Staff import Staff 

parser = argparse.ArgumentParser()
parser.add_argument(
    '-k', 
    '--keys', 
    help='provide path to admin keys', 
    default='../_keys/adminKeys.py', 
    metavar=''
)
args = parser.parse_args()
auth = Authentication(args.keys) if args.keys else Authentication()

# Create staff object
staff = Staff('', auth)
with open('user-list.txt', 'r') as json_file:
    allUsers = json.load(json_file)
    # Reset all passwords and save to csv
    for user in allUsers['users']: staff.resetPassword(user)

      
# COMMENT OUT TO STOP REMOVAL OF ADMIN KEYS AFTER SCRIPT EXIT (not recommended)
if staff.auth.removeKeys(): print('Keys safely removed from working directory')
else: print('Keys not removed from working directory.')
