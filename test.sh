#!/bin/bash

REGION=${AWS_REGION:-eu-west-1}

echo "Fetching API Gateway invoke URL..."
api_id=$(aws apigateway get-rest-apis \
  --region ${REGION} \
  --query "items[?name=='whats_my_ip'].id" \
  --output text)

api_url="https://${api_id}.execute-api.${REGION}.amazonaws.com/dev/ip"

echo "Querying cloudformation..."
echo "POST request"
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"id":"123", "name":"Name"}' \
   "$api_url"

 curl -X GET "$api_url"