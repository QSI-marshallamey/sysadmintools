#!/usr/bin/sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

aws configure sso
#SSO start URL: [https://quantumsi.awsapps.com/start]
#SSO Region: [us-east-1]

#CLI default client Region: [us-east-1]
#CLI default output format: [json]
#CLI profile name: [default]

aws sso login