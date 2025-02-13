#!/usr/bin/env python3

### [ECR.2] ECR private repositories should have tag immutability configured
### This control checks whether a private ECR repository has tag immutability enabled. 
### This control fails if a private ECR repository has tag immutability disabled. 
### This rule passes if tag immutability is enabled and has the value IMMUTABLE. 

# This script configures image scanning on a private ECR repository.  
# A repo argument is optional. If no repo argument, all repos will have image scanning enabled
# This configuration method is deprecated in favor of enabling scanning at the registry level.  
# This script also performs that task, however, you will not pass security check without 
# using the deprecated method as well.

from datetime import datetime
import argparse
import logging
import sys
from AWS import AWS

### PARSE ARGUMENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--repo', 
    help='Name of the ECR repository. If no repo argument, all repositories will have image scanning enabled.',  
    metavar=''
)
args = parser.parse_args()


### LOGGER FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
logging.basicConfig(
    filename=f'../log/{datetime.now().strftime("%Y-%m-%d-%H:%M")}-aws-ecr-enable-tag-immutability.log', 
    filemode='w', 
    format='%(message)s',
  level=logging.INFO
)
# Print all logs to screen
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


### MAIN FUNCTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
ECR_REPOS = [ AWS().getRepos(args.repo) ] if args.repo else AWS().getRepos()
for repo in ECR_REPOS:
    if repo['imageTagMutability'] == 'IMMUTABLE':
        logging.warning(f"WARNING: Tag immutability already enabled on {repo['repositoryName']}. Skipping...\n")
    else: 
        #input('Waiting for you')
        response = AWS().enableTagImmutability(repo['repositoryName'], repo['registryId']) 
        if response and response['imageTagMutability'] == 'IMMUTABLE':
            logging.info(f"SUCCESS: Tag immutability enabled on {response['repositoryName']}.\n")
        else: logging.error(f"ERROR: Tag immutability NOT enabled on {repo['repositoryName']}.\n")