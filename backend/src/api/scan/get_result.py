"""
Get scan result API endpoint.
"""
from typing import Dict, Any

from src.db.db_repositories import scan_repository
from src.utils.utils_response import success_response, error_response
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Get complete scan results.
    
    GET /scan/{scan_id}/result
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API response with complete scan results
    """
    try:
        # Extract user ID from authorizer context
        user_id = event.get('requestContext', {}).get('authorizer', {}).get('user_id', 'anonymous')
        
        # Extract scan ID from path parameters
        scan_id = event.get('pathParameters', {}).get('scan_id')
        
        if not scan_id:
            return error_response("Scan ID is required", 400)
        
        logger.info("Get scan result", scan_id=scan_id, user_id=user_id)
        
        # Fetch scan from database
        scan = scan_repository.get_scan(user_id, scan_id)
        
        if not scan:
            return error_response(
                "Scan not found",
                404,
                "SCAN_NOT_FOUND"
            )
        
        # Check if scan is completed
        if scan['status'] != 'COMPLETED':
            return error_response(
                f"Scan is not completed yet (status: {scan['status']})",
                400,
                "SCAN_NOT_COMPLETED"
            )
        
        # Build complete result
        result_data = {
            "scan_id": scan['scan_id'],
            "user_id": scan['user_id'],
            "target": scan['target'],
            "scan_type": scan['scan_type'],
            "environment": scan.get('environment'),
            "status": scan['status'],
            "created_at": scan['created_at'],
            "started_at": scan.get('started_at'),
            "completed_at": scan.get('completed_at'),
            "tool_results": scan.get('tool_results', []),
            "score": scan.get('score', {}),
            "recommendations": _generate_recommendations(scan)
        }
        
        logger.info("Scan result retrieved", scan_id=scan_id)
        
        return success_response(result_data)
        
    except Exception as e:
        logger.error("Get scan result error", error=str(e))
        return error_response(
            message="Failed to get scan result",
            status_code=500,
            error_code="INTERNAL_ERROR",
            details={"error": str(e)}
        )


def _generate_recommendations(scan: Dict) -> list:
    """
    Generate prioritized recommendations based on scan results.
    
    Args:
        scan: Scan data
        
    Returns:
        List of recommendations
    """
    recommendations = []
    score_data = scan.get('score', {})
    
    # Critical issues recommendation
    if score_data.get('critical_count', 0) > 0:
        recommendations.append({
            "priority": "CRITICAL",
            "title": "Address Critical Security Issues Immediately",
            "description": f"Found {score_data['critical_count']} critical security issues that require immediate attention.",
            "action": "Review critical findings and implement fixes as highest priority"
        })
    
    # High severity recommendation
    if score_data.get('high_count', 0) > 0:
        recommendations.append({
            "priority": "HIGH",
            "title": "Fix High Severity Vulnerabilities",
            "description": f"Identified {score_data['high_count']} high severity security issues.",
            "action": "Plan remediation for high severity issues within the next sprint"
        })
    
    # Score-based recommendations
    score = score_data.get('score', 100)
    if score < 70:
        recommendations.append({
            "priority": "MEDIUM",
            "title": "Improve Overall Security Posture",
            "description": f"Current security score is {score}/100, indicating significant security gaps.",
            "action": "Implement a security improvement roadmap and track progress"
        })
    
    # Headers recommendation
    tool_results = scan.get('tool_results', [])
    headers_result = next((r for r in tool_results if r.get('tool') == 'headers'), None)
    if headers_result and headers_result.get('severity', {}).get('high', 0) > 0:
        recommendations.append({
            "priority": "MEDIUM",
            "title": "Configure Security Headers",
            "description": "Missing critical security headers expose the application to attacks.",
            "action": "Add Strict-Transport-Security, CSP, and other security headers"
        })
    
    # TLS recommendation
    tls_result = next((r for r in tool_results if r.get('tool') == 'tls'), None)
    if tls_result and tls_result.get('severity', {}).get('high', 0) > 0:
        recommendations.append({
            "priority": "HIGH",
            "title": "Update TLS Configuration",
            "description": "TLS configuration issues detected that may compromise encryption.",
            "action": "Update to TLS 1.2+ and use strong cipher suites"
        })
    
    return recommendations[:5]  # Return top 5 recommendations