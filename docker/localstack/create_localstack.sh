#!/bin/bash

echo 'Creating SQS'

awslocal sqs create-queue --queue-name transaction-queue --attributes VisibilityTimeout=60
awslocal sqs create-queue --queue-name invalidation-queue --attributes VisibilityTimeout=120
awslocal s3api create-bucket --bucket igvf-files-local --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
