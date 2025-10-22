#!/bin/bash

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

echo "Fetching API Gateway invoke URL..."
api_id=$(aws apigateway get-rest-apis \
  --region eu-west-1 \
  --query "items[?name=='whats_my_ip'].id" \
  --output text)

api_url="https://${api_id}.execute-api.eu-west-1.amazonaws.com/dev/ip"

echo "Querying cloudformation..."
echo "POST request"
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"id":"123", "name":"Name"}' \
   "$api_url"

 curl -X GET "$api_url"