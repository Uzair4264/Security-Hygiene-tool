"""
Get scan status API endpoint.
"""
from typing import Dict, Any

from src.db.db_repositories import scan_repository
from src.utils.utils_response import success_response, error_response
from src.utils.utils_logger import get_logger



logger = get_logger(__name__)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get scan status.
    
    GET /scan/{scan_id}/status
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API response with scan status
    """
    try:
        # Extract user ID from authorizer context
        user_id = event.get('requestContext', {}).get('authorizer', {}).get('user_id', 'anonymous')
        
        # Extract scan ID from path parameters
        scan_id = event.get('pathParameters', {}).get('scan_id')
        
        if not scan_id:
            return error_response("Scan ID is required", 400)
        
        logger.info("Get scan status", scan_id=scan_id, user_id=user_id)
        
        # Fetch scan from database
        scan = scan_repository.get_scan(user_id, scan_id)
        
        if not scan:
            return error_response(
                "Scan not found",
                404,
                "SCAN_NOT_FOUND"
            )
        
        # Extract status information
        status_data = {
            "scan_id": scan['scan_id'],
            "status": scan['status'],
            "target": scan['target'],
            "scan_type": scan['scan_type'],
            "created_at": scan['created_at'],
            "started_at": scan.get('started_at'),
            "completed_at": scan.get('completed_at')
        }
        
        # Add error if present
        if scan.get('error'):
            status_data['error'] = scan['error']
        
        # Add score summary if completed
        if scan['status'] == 'COMPLETED' and scan.get('score'):
            status_data['score'] = {
                'value': scan['score']['score'],
                'grade': scan['score']['grade']
            }
        
        logger.info("Scan status retrieved", scan_id=scan_id, status=scan['status'])
        
        return success_response(status_data)
        
    except Exception as e:
        logger.error("Get scan status error", error=str(e))
        return error_response(
            message="Failed to get scan status",
            status_code=500,
            error_code="INTERNAL_ERROR",
            details={"error": str(e)}
        )