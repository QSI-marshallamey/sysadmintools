#!/usr/bin/env python3

### [SNS.1] SNS topics should be encrypted at rest using AWS KMS
### This control checks whether an SNS topic is encrypted at rest using AWS KMS.

import argparse
import logging
import sys
from datetime import datetime
from AWS import AWS

### PARSE ARGUMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--topics', 
    help='Comma-separated list of SNS Topics. If no topics argument, all topics will have encryption enabled.',  
    metavar=''
)
parser.add_argument('-p', '--profile', 
    help='AWS account profile to use for this run.  Default is default',  
    default='default',
    metavar=''
)
args = parser.parse_args()


### LOGGER FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
logging.basicConfig(
    filename=f'../log/{datetime.now().strftime("%Y-%m-%d-%H:%M")}-aws-sns-enable-encryption.log', 
    filemode='w', 
    format='%(message)s',
    level=logging.INFO
)
# Print all logs to screen
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


### MAIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
aws = AWS(profile=args.profile)
TOPICS = args.topics.split(',') if args.topics else aws.listTopics()
for topic in TOPICS:
    logging.info(f"INFO: Looking for encryption policy on {topic}...")
    attributes = aws.getTopicAttributes(topic['TopicArn'])
    logging.info(f'INFO: CURRENT ATTRIBUTES ==>  {attributes}')
    if not attributes:
        logging.error(f"ERROR: Unable to retrieve encryption policy for {topic['TopicArn']}. Skipping...\n")
        continue
    if 'KmsMasterKeyId' not in attributes:
        encryptionEnabled = aws.enableTopicEncryption(topic['TopicArn'], 'alias/aws/sns')
        if encryptionEnabled: 
            logging.info(f"INFO: Encryption at rest now enabled on {topic['TopicArn']}\n")
        else: 
            logging.info(f"ERROR: Encryption not enabled on {topic['TopicArn']}.\n")
    else: 
        logging.warning(f"WARN: Found existing encryption policy on {topic['TopicArn']}. Skipping...\n")
        continue
