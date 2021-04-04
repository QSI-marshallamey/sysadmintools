
import argparse
import json
from datetime import datetime

from lib.Authentication import Authentication
from lib.Communication import Communication

parser = argparse.ArgumentParser()
parser.add_argument(
    '-k', 
    '--keys', 
    help='provide path to admin keys', 
    default='../_keys/adminKeys.py', 
    metavar=''
)
args = parser.parse_args()

if args.keys: auth = Authentication(args.keys) 
else: auth = Authentication()

c = Communication(auth)
c.sendSMS('2102597513', 'Hey Marshall!!')
c.sendEmail('marshall@clouddev.ninja', 'Subject: TEST MESSAGE2\nThis is a test message.  Hello WORLD!')
c.getEmail()