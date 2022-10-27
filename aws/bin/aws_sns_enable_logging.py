#!/usr/bin/env python3

### [SNS.2] Logging of delivery status should be enabled for notification messages sent to a topic
### This control checks whether logging is enabled for the delivery status of notification messages
### sent to an Amazon SNS topic for the endpoints. This control fails if the delivery status 
### notification for messages is not enabled.

import argparse
import logging
import sys
from datetime import datetime
from AWS import AWS as aws

### PARSE ARGUMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--topics', 
    help='Comma-separated list of SNS Topics. If no topics argument, all topics will have logging enabled.',  
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
    filename=f'../log/{datetime.now().strftime("%Y-%m-%d-%H:%M")}-aws-sns-enable-logging.log', 
    filemode='w', 
    format='%(message)s',
    level=logging.INFO
)
# Print all logs to screen
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


### MAIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AWS = aws(profile=args.profile)
TOPICS = args.topics.split(',') if args.topics else AWS.listTopics()
for topic in TOPICS:
    logging.info(f"INFO: Looking for logging policy on {topic}...")
    attributes = AWS.getTopicAttributes(topic['TopicArn'])
    logging.info(f'INFO: CURRENT ATTRIBUTES ==>  {attributes}')
    if not attributes:
        logging.error(f"ERROR: Unable to retrieve topic attributes for {topic['TopicArn']}. Skipping...\n")
        continue
    if (
        'HTTPFailureFeedbackRoleArn' not in attributes or
        'HTTPSuccessFeedbackRoleArn' not in attributes or
        'HTTPSuccessFeedbackSampleRate' not in attributes
    ):
        loggingEnabled = AWS.enableTopicLogging(topic['TopicArn'])
        if loggingEnabled: 
            logging.info(f"INFO: Logging now enabled on {topic['TopicArn']}\n")
        else: 
            logging.info(f"ERROR: Logging not enabled on {topic['TopicArn']}.\n")
    else: 
        logging.warning(f"WARN: Found existing logging policy on {topic['TopicArn']}. Skipping...\n")
        continue


# TODO #Create IAM Roles
# SNSSuccessFeedback
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "logs:CreateLogGroup",
#         "logs:CreateLogStream",
#         "logs:PutLogEvents",
#         "logs:PutMetricFilter",
#         "logs:PutRetentionPolicy"
#       ],
#       "Resource": [
#         "*"
#       ]
#     }
#   ]
# }

# SNSFailureFeedback
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "logs:CreateLogGroup",
#         "logs:CreateLogStream",
#         "logs:PutLogEvents",
#         "logs:PutMetricFilter",
#         "logs:PutRetentionPolicy"
#       ],
#       "Resource": [
#         "*"
#       ]
#     }
#   ]
# }