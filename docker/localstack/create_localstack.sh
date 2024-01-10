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
