#!/bin/bash

echo 'Creating SQS'

awslocal sqs create-queue --queue-name transaction-queue --attributes VisibilityTimeout=60
awslocal sqs create-queue --queue-name invalidation-queue --attributes VisibilityTimeout=120
