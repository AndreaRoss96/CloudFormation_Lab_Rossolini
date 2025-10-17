#!/bin/bash

echo "test"

echo "Zipping deployment package..."
zip -r index.zip index.app

echo "Uploading to s3..."
aws s3 cp index.zip s3://my-lambda-code-bucket/app.zip

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-lambda-rest-api \
  --parameter-overrides S3BucketName=my-lambda-code-bucket S3Key=index.zip \
  --capabilities CAPABILITY_IAM

echo "Querying cloudformation..."
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"id":"123", "name":"Name"}' \
   https://abcd1234.execute-api.eu-west-1.amazonaws.com/dev/ip
