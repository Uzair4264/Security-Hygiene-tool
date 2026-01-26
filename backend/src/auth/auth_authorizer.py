"""
Lambda authorizer for API Gateway.
"""
from typing import Dict, Any

from src.auth.auth_jwt import validate_token
from src.config.config_settings import settings
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


def generate_policy(
    principal_id: str,
    effect: str,
    resource: str,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Generate IAM policy for API Gateway.
    
    Args:
        principal_id: User identifier
        effect: Allow or Deny
        resource: API Gateway resource ARN
        context: Optional context to pass to Lambda
        
    Returns:
        IAM policy document
    """
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
    }
    
    if context:
        policy['context'] = context
    
    return policy


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda authorizer handler.
    
    Args:
        event: API Gateway authorizer event
        context: Lambda context
        
    Returns:
        IAM policy
        
    Raises:
        Exception: If authorization fails
    """
    try:
        # Get token from Authorization header
        token = event.get('authorizationToken', '')
        method_arn = event.get('methodArn', '')
        
        logger.info("Authorizer invoked", method_arn=method_arn)
        
        # Check if anonymous mode is enabled
        if settings.ALLOW_ANONYMOUS:
            logger.info("Anonymous mode enabled, allowing request")
            return generate_policy(
                principal_id='anonymous',
                effect='Allow',
                resource=method_arn,
                context={'user_id': 'anonymous'}
            )
        
        # Validate token
        is_valid, user_id, error = validate_token(token)
        
        if not is_valid:
            logger.warning("Authorization failed", error=error)
            raise Exception('Unauthorized')
        
        logger.info("Authorization successful", user_id=user_id)
        
        # Return policy allowing the request
        return generate_policy(
            principal_id=user_id,
            effect='Allow',
            resource=method_arn,
            context={'user_id': user_id}
        )
        
    except Exception as e:
        logger.error("Authorizer error", error=str(e))
        raise Exception('Unauthorized')