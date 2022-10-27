#!/usr/bin/env python3

### [S3.5] S3 buckets should require requests to use Secure Socket Layer
### This control checks whether S3 buckets have policies that require requests
### to use Secure Socket Layer (SSL).

import sys
from datetime import datetime
import argparse
import logging
import json
from AWS import AWS

### PARSE ARGUMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--buckets', 
    help='Comma-separated list of the S3 bucket names. If no buckets argument, all buckets will have SSL enforced.',  
    metavar=''
)
args = parser.parse_args()


### LOGGER FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
logging.basicConfig(
    filename=f'../log/{datetime.now().strftime("%Y-%m-%d-%H:%M")}-aws-s3-require-ssl.log', 
    filemode='w', 
    format='%(message)s',
    level=logging.INFO
)
# Print all logs to screen
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


### MAIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def SSLPolicyInStatement(policy):
    if any(statement['Sid'] == 'AllowSSLRequestsOnly' for \
    statement in policy['Statement'] if 'Sid' in statement): return True
    else: return False

S3_BUCKETS = [ AWS(profile='chips').getBucket(args.buckets) ] if args.buckets else AWS(profile='chips').listBuckets()
for bucket in S3_BUCKETS:

    DEFAULT_SSL_POLICY = {
        'Version': '2012-10-17',
        'Statement': [{
            "Sid": "AllowSSLRequestsOnly",
            "Action": "s3:*",
            "Effect": "Deny",
            "Resource": [
                f"arn:aws:s3:::{bucket['Name']}",
                f"arn:aws:s3:::{bucket['Name']}/*"
            ],
            "Condition": {
                "Bool": {
                        "aws:SecureTransport": "false"
                }
            },
            "Principal": "*"
        }]
    }

    policy = AWS(profile='chips').getBucketPolicy(bucket['Name'])
    if policy: policy = json.loads(policy)
    if policy and SSLPolicyInStatement(policy): 
        logging.warn(f"WARN: SSL already enforced on {bucket['Name']}\n{policy}\n")
        continue
    elif policy: policy['Statement'].append(DEFAULT_SSL_POLICY['Statement'][0])
    else: policy = DEFAULT_SSL_POLICY

    if AWS(profile='chips').requireSSL(bucket['Name'], json.dumps(policy)):
        logging.info(f"INFO: SSL now enforced on {bucket['Name']}\n{policy}\n")
    else: logging.info(f"ERROR: SSL not enforced on {bucket['Name']}.\n")
    