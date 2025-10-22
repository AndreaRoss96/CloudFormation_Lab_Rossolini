#!/bin/bash
set -euo pipefail

STACK_NAME="lambda-rest-dynamodb"
S3_BUCKET="$1"   # bucket to upload lambda zip and use with cloudformation package
CODE_KEY="index.zip"
REGION=${AWS_REGION:-eu-west-1}

echo "Zipping deployment package..."
zip -r ${CODE_KEY} index.app

echo "Uploading to s3..."
aws s3 cp ${CODE_KEY} s3://${S3_BUCKET}/${CODE_KEY} --region ${REGION}

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name ${STACK_NAME} \
  --parameter-overrides S3BucketName=${S3_BUCKET} S3Key=${CODE_KEY} \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region ${REGION}

echo "Done. Outputs:"
aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[0].Outputs" --region ${REGION} --output table

