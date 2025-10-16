import os
import json
import logging # http://realpython.com/python-logging/

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") # verbosity control
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

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
        return False, "Payload must be a JSON object."
    if "id" not in payload or not isinstance(payload.get("id"), str) or payload["id"].strip() == "":
        return False, "Field 'id' is required and must be a non-empty string"
    if "name" not in payload or not isinstance(payload.get("name"), str):
        return False, "Field 'name' is required and must be a string"
    return True, None

def lambda_handler(event, context):
    method = event.get("httpMethod")
    if method == "GET":
        return response(200,
            {
                "message": "POST received",
                "data": {"message": "GET request received"}
            })
    elif method == "POST":
        body = json.loads(event.get("body", "{}"))
        ok, err = validate_item(context.body)
        if not ok :
            return response(400, {"error" : err})
        return response(200,
            {
                "message": "POST received",
                "data": body
            })
        }
    else:
        return response(405,
            {"error": "Method not allowed"})



