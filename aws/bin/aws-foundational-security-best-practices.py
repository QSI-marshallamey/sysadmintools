#!/usr/bin/env python3

# ######################### CLOUDFORMATION (CF)  #########################
# ##########  CLOUDFORMATION.1  ###########
# aws-cf-enable-event-notifications

# ######################### ELASTIC CONTAINER REGISTRY (ECR)  #########################
# ################  ECR.1  ################
# aws-ecr-enable-image-scanning
# ################  ECR.2  ################
import aws_ecr_enable_tag_immutability
# ################  ECR.3  ################
# aws-ecr-enable-lifecycle-policy

# ######################### ELASTIC CONTAINER SERVICE (ECS)  #########################
# ################  ECS.1  ################
# aws-ecs-secure-networking-modes
# ################  ECS.2  ################
# aws-ecs-disable-auto-public-ip
# ################  ECS.3  ################
# aws-ecs-disable-host-process-sharing
# ################  ECS.4  ################
# aws-ecs-remove-container-privilege
# ################  ECS.5  ################
# aws-ecs-make-containers-read-only
# ################  ECS.8  ################
# aws-ecs-disable-secrets-as-env-variables
# ################  ECS.10  ################
# aws-ecs-upgrade-fargate-version
# ################  ECS.12  ################
# aws-ecs-enable-container-insights


# ######################### S3  #########################
# #################  S3.1  #################
# aws-s3-account-block-public-access
# ############ S3.2  S3.3  S3.8 ############
# aws-s3-bucket-block-public-access
# #################  S3.4  #################
# aws-s3-enable-encryption
# #################  S3.5  #################
# aws-s3-require-ssl
# #################  S3.6  #################
# aws-s3-restrict-cross-account-access
# #################  S3.9  #################
# aws-s3-enable-bucket-access-logging
# #################  S3.10  #################
# aws-s3-enable-versioning
# #################  S3.11  #################
# aws-s3-enable-event-notifications
# #################  S3.12  #################
# aws-s3-disable-acls
# #################  S3.13  #################
# aws-s3-configure-lifecyle-policy

# ######################### SIMPLE QUEUE SERVICE (SQS)  #########################
# ################  SQS.1  ################
# aws-sqs-enable-encryption