#!/usr/bin/env python3

### [SQS.1] Amazon SQS queues should be encrypted at rest
### This control checks whether Amazon SQS queues are encrypted at rest. 
### The control passes if you use an Amazon SQS managed key (SSE-SQS) or 
### an AWS Key Management Service (AWS KMS) key (SSE-KMS).

import argparse
import logging
import sys
from datetime import datetime
from AWS import AWS

### PARSE ARGUMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parser = argparse.ArgumentParser()
parser.add_argument('-q', '--queues', 
    help='Comma-separated list of SQS Queues. If no queues argument, all queues will have encryption enabled.',  
    metavar=''
)
args = parser.parse_args()


### LOGGER FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
logging.basicConfig(
    filename=f'../log/{datetime.now().strftime("%Y-%m-%d-%H:%M")}-aws-sqs-enable-encryption.log', 
    filemode='w', 
    format='%(message)s',
    level=logging.INFO
)
# Print all logs to screen
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


### MAIN FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def main():
    QUEUES = AWS().listQueues()
    
    if QUEUES:
        for queue in QUEUES:
            logging.info(f"INFO: Looking for encryption policy on {queue}...")
            attributes = AWS().getQueueAttributes(queue)
            logging.info(f'INFO: CURRENT ATTRIBUTES ==>  {attributes}')
            if attributes['SqsManagedSseEnabled'] == 'false': 
                encryptionEnabled = AWS().enableQueueEncryption(queue, { 'SqsManagedSseEnabled': 'true' })
                if encryptionEnabled: 
                    logging.info(f"INFO: Encryption at rest now enabled on {queue}\n")
                else: 
                    logging.info(f"ERROR: Encryption not enabled on {queue}.\n")
            else: 
                logging.warning(f"WARN: Found existing encryption policy on {queue}. Skipping...\n")
                continue

if __name__ == '__main__': main()