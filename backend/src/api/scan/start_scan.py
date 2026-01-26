"""
Start scan API endpoint.
"""
import time  
import json
import uuid
from typing import Dict, Any
import threading
import os
def run_local_scan(scan_id: str, user_id: str, target: str, scan_type: str):
    """
    Run scan orchestration locally in background.
    """
    time.sleep(1) 
    try:
        from core.core_orchestrator import ScanOrchestrator

        orchestrator = ScanOrchestrator(
            scan_id=scan_id,
            user_id=user_id,
            target=target,
            scan_type=scan_type
        )
        orchestrator.execute()

    except Exception as e:
        logger.error(
            "Local scan execution failed",
            scan_id=scan_id,
            error=str(e)
        )

import boto3 
from pydantic import ValidationError

from src.models.models_scan_request import ScanRequest
from src.db.db_repositories import scan_repository
from src.utils.utils_response import success_response, error_response, validation_error_response
from src.utils.utils_validators import validate_url, validate_github_repo
from src.config.config_settings import settings
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Start a security scan.
    
    POST /scan/start
    
    Body:
    {
        "target": "https://example.com",
        "scan_type": "quick" | "full",
        "environment": "dev" | "staging" | "production" (optional),
        "github_repo": "https://github.com/user/repo" (optional)
    }
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API response with scan_id
    """
    try:
        # Extract user ID from authorizer context
        user_id = event.get('requestContext', {}).get('authorizer', {}).get('user_id', 'anonymous')
        
        logger.info("Start scan requested", user_id=user_id)
        
        # Parse request body
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return error_response("Invalid JSON in request body", 400)
        
        # Validate request
        try:
            scan_request = ScanRequest(**body)
        except ValidationError as e:
            errors = {}
            for error in e.errors():
                field = error['loc'][0]
                errors[str(field)] = error['msg']
            return validation_error_response(errors)
        
        # Additional validation
        is_valid, error_msg = validate_url(scan_request.target)
        if not is_valid:
            return error_response(error_msg, 400, "INVALID_URL")
        
        if scan_request.github_repo:
            is_valid, error_msg = validate_github_repo(scan_request.github_repo)
            if not is_valid:
                return error_response(error_msg, 400, "INVALID_REPO")
        
        # Generate scan ID
        scan_id = str(uuid.uuid4())
        
        # Create scan record
        scan_repository.create_scan(
            scan_id=scan_id,
            user_id=user_id,
            target=scan_request.target,
            scan_type=scan_request.scan_type.value,
            environment=scan_request.environment.value if scan_request.environment else None,
            github_repo=scan_request.github_repo
        )
        
                # Trigger scan execution
        if os.getenv("LOCAL_MODE") == "true":
            logger.info("Running scan locally", scan_id=scan_id)

            thread = threading.Thread(
                target=run_local_scan,
                args=(
                    scan_id,
                    user_id,
                    scan_request.target,
                    scan_request.scan_type.value
                ),
                daemon=True
            )
            thread.start()

        else:
            # AWS Lambda invocation
            try:
                lambda_client = boto3.client('lambda', region_name=settings.AWS_REGION)

                payload = {
                    'scan_id': scan_id,
                    'user_id': user_id,
                    'target': scan_request.target,
                    'scan_type': scan_request.scan_type.value
                }

                lambda_client.invoke(
                    FunctionName=settings.LAMBDA_FUNCTION_NAME_SCAN_PROCESSOR,
                    InvocationType='Event',
                    Payload=json.dumps(payload)
                )

                logger.info("Scan processor invoked", scan_id=scan_id)

            except Exception as e:
                logger.error(
                    "Failed to invoke scan processor",
                    scan_id=scan_id,
                    error=str(e)
                )

        
        response_data = {
            "scan_id": scan_id,
            "status": "PENDING",
            "message": "Scan initiated successfully"
        }
        
        logger.info("Scan created", scan_id=scan_id, user_id=user_id)
        
        return success_response(response_data, 202)
        
    except Exception as e:
        logger.error("Start scan error", error=str(e))
        return error_response(
            message="Failed to start scan",
            status_code=500,
            error_code="INTERNAL_ERROR",
            details={"error": str(e)}
        )