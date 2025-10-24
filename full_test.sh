#!/usr/bin/env bash
set -euo pipefail

#  CONFIGURATION 
REGION="${AWS_REGION:-eu-west-1}"
API_NAME="${API_NAME:-whats_my_ip}"
STAGE="${STAGE:-dev}"
RESOURCE_PATH="${RESOURCE_PATH:-ip}"

ID="${1:-123}"
NAME="${2:-TestName}"

# PRECHECKS 
for cmd in aws jq curl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "❌ Required command '$cmd' not found. Please install it first."
    exit 1
  fi
done

echo "Fetching API Gateway invoke URL for '${API_NAME}' in region '${REGION}'..."
api_id=$(aws apigateway get-rest-apis \
  --region "${REGION}" \
  --query "items[?name=='${API_NAME}'].id" \
  --output text)

if [[ -z "$api_id" || "$api_id" == "None" ]]; then
  echo "ERROR: API Gateway '${API_NAME}' not found in region '${REGION}'."
  exit 1
fi

api_url="https://${api_id}.execute-api.${REGION}.amazonaws.com/${STAGE}/${RESOURCE_PATH}"
echo "Using API URL: ${api_url}"
echo

# TEST: POST REQUEST 
echo "Sending POST request..."
post_body=$(jq -n --arg id "$ID" --arg name "$NAME" '{id: $id, name: $name}')
echo "Request body: $post_body"

post_response=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -d "$post_body" \
  "$api_url")

# Split body and status
post_body_resp=$(echo "$post_response" | head -n1)
post_status=$(echo "$post_response" | tail -n1)

echo "Response status: $post_status"
echo "Response body: $post_body_resp" | jq || echo "$post_body_resp"

if [[ "$post_status" != "200" ]]; then
  echo "POST request failed."
  exit 1
fi

# TEST: GET REQUEST 
echo
echo "Sending GET request for id=${ID}..."
get_response=$(curl -s -w "\n%{http_code}" -X GET "${api_url}/${ID}")
get_body_resp=$(echo "$get_response" | head -n1)
get_status=$(echo "$get_response" | tail -n1)

echo "Response status: $get_status"
echo "Response body: $get_body_resp" | jq || echo "$get_body_resp"

if [[ "$get_status" != "200" ]]; then
  echo "GET request failed."
  exit 1
fi

echo
echo "All tests passed"
