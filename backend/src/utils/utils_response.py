"""
HTTP response utilities for API Gateway.
"""
import json
from typing import Any, Dict, Optional


def success_response(
    data: Any,
    status_code: int = 200,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a successful API Gateway response.
    
    Args:
        data: Response data
        status_code: HTTP status code
        message: Optional success message
        
    Returns:
        API Gateway response dict
    """
    body = {
        "success": True,
        "data": data
    }
    
    if message:
        body["message"] = message
    
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(body)
    }


def error_response(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create an error API Gateway response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Optional error code
        details: Optional additional error details
        
    Returns:
        API Gateway response dict
    """
    body = {
        "success": False,
        "error": {
            "message": message
        }
    }
    
    if error_code:
        body["error"]["code"] = error_code
    
    if details:
        body["error"]["details"] = details
    
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(body)
    }


def validation_error_response(
    errors: Dict[str, str]
) -> Dict[str, Any]:
    """
    Create a validation error response.
    
    Args:
        errors: Dictionary of field errors
        
    Returns:
        API Gateway response dict
    """
    return error_response(
        message="Validation failed",
        status_code=400,
        error_code="VALIDATION_ERROR",
        details={"fields": errors}
    )