#!/bin/bash

echo 'Creating DLQ'

TRANSACTION_DLQ_URL=$(awslocal sqs create-queue --queue-name transaction-dead-letter-queue --query 'QueueUrl' --output text)
TRANSACTION_DLQ_ARN=$(awslocal sqs get-queue-attributes --queue-url $TRANSACTION_DLQ_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

echo $TRANSACTION_DLQ_URL

INVALIDATION_DLQ_URL=$(awslocal sqs create-queue --queue-name invalidation-dead-letter-queue --query 'QueueUrl' --output text)
INVALIDATION_DLQ_ARN=$(awslocal sqs get-queue-attributes --queue-url $INVALIDATION_DLQ_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

echo $INVALIDATION_DLQ_URL

echo 'Creating SQS'

awslocal sqs create-queue --queue-name transaction-queue --attributes '{"RedrivePolicy": "{\"deadLetterTargetArn\":\"'$TRANSACTION_DLQ_ARN'\",\"maxReceiveCount\":\"3\"}", "VisibilityTimeout": "60"}'
awslocal sqs create-queue --queue-name invalidation-queue --attributes '{"RedrivePolicy": "{\"deadLetterTargetArn\":\"'$INVALIDATION_DLQ_ARN'\",\"maxReceiveCount\":\"3\"}", "VisibilityTimeout": "120"}'

echo 'Creating S3 buckets'

S3_BUCKET=$(awslocal s3api create-bucket --bucket igvf-files-local --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2 --query 'Location' --output text)
RESTRICTED_S3_BUCKET=$(awslocal s3api create-bucket --bucket igvf-restricted-files-local --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2 --query 'Location' --output text)

echo $S3_BUCKET
echo $RESTRICTED_S3_BUCKET
