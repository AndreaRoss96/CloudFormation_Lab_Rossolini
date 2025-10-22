import os
import json
import logging
import boto3

# Logging configs
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") # verbosity control
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# DynamoDB setup
TABLE_NAME = os.getenv("TABLE_ENV", "ItemsTable")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

#region Utility Functions
def response(status_code, body):
    """
    Wrap data into HTTP format 
    """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def validate_item(payload):
    """
    Ensure the POST body has the essential fields id and name and the correct format
    """
    if not isinstance(payload, dict):
        msg = "Payload must be a JSON object."
        logger.warning(f"Validation failed: {msg}")
        return False, 
    if "id" not in payload or not isinstance(payload.get("id"), str) or payload["id"].strip() == "":
        msg = "Field 'id' is required and must be a non-empty string"
        logger.warning(f"Validation failed: {msg}")
        return False, 
    if "name" not in payload or not isinstance(payload.get("name"), str):
        msg = "Field 'name' is required and must be a string"
        logger.warning(f"Validation failed: {msg}")
        return False, 
    logger.debug(f"Validation passed for payload: {payload}")
    return True, None
#endregion

def get_item(event):
    logger.info(f"GET request processed for Request ID {request_id}")
    params = event.get("pathParameters") or {}
    item_id = params.get("id") if params else None
    if not item_id:
        return response(400, {"error": "Missing query parameter: id"})
    
    try:
        res = table.get_item(Key={"id": item_id})
        item = res.get("Item")
        if not item:
            return response(404, {"error": "Item not found"})
        logger.info(f"Retrieved item: {item}")
        return response(200, {"item": item})
    except ClientError as e:
        logger.error(f"DynamoDB Get Error: {e}")
        return response(500, {"error": "DynamoDB read failed"})


def post_item(event):
    body = json.loads(event.get("body", "{}"))
    ok, err = validate_item(body)
    if not ok:
        logger.error(f"Validation error for request {request_id}: {err}")
        return response(400, {"error": err})

    try:
        table.put_item(Item=body)
        logger.info(f"POST processed successfully for request {request_id}")
        return response(200, {"message": "POST received", "data": body})
    except ClientError as e:
        logger.error(f"DynamoDB Error: {e}")
        return response(500, {"error": "DynamoDB write failed"})
        

def lambda_handler(event, context):
    request_id = getattr(context, "aws_request_id", "N/A")
    method = event.get("httpMethod")

    logger.info(f"Request {request_id} received: method={method}")
    logger.debug(f"Full event: {json.dumps(event)}")

    try:
        if method == "GET":
            return get_item(event)
        elif method == "POST":
            return post_item(event)
        else:
            logger.warning(f"Unsupported HTTP method {method} in request {request_id}")
            return response(405, {"error": "Method not allowed"})
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        return response(500, {"error": "Internal server error"}) 



