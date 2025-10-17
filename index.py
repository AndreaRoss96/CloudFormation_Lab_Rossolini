import os
import json
import logging # http://realpython.com/python-logging/

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") # verbosity control
logging.basicConfig(
    level=LOG_LEVEL
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

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

def lambda_handler(event, context):
    request_id = getattr(context, "aws_request_id", "N/A")
    method = event.get("httpMethod")

    logger.info(f"Request {request_id} received: method={method}")
    logger.debug(f"Full event: {json.dumps(event)}")

    if method == "GET":
        logger.info(f"GET request processed for Request ID {request_id}")
        return response(200,
            {
                "message": "POST received",
                "data": {"message": "GET request received"}
            })
    elif method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in POST request {request_id}")
            return response(400, {"error": "Invalid JSON payload."})

        ok, err = validate_item(body)
        if not ok:
            logger.error(f"Validation error for request {request_id}: {err}")
            return response(400, {"error": err})

        logger.info(f"POST processed successfully for request {request_id}")
        return response(200, {"message": "POST received", "data": body})
    else:
        logger.warning(f"Unsupported HTTP method {method} in request {request_id}")
        return response(405, {"error": "Method not allowed"})



