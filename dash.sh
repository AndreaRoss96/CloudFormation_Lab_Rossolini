#!/bin/bash

echo "test"

echo "Zipping deployment package..."
zip -r index.zip index.app

echo "Uploading to s3..."
aws s3 cp index.zip s3://my-lambda-code-bucket/app.zip

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name lambda-rest-dynamodb \
  --parameter-overrides S3BucketName=my-lambda-bucket-00196817 S3Key=index.zip \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region eu-west-1 
  
echo "Querying cloudformation..."
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"id":"123", "name":"Name"}' \
   https://abcd1234.execute-api.eu-west-1.amazonaws.com/dev/ip
