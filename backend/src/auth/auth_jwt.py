"""
JWT token validation and utilities.
"""
import jwt
from typing import Dict, Optional
from jose import JWTError

from src.config.config_settings import settings
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


def decode_jwt(token: str) -> Optional[Dict]:
    """
    Decode and validate JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Decode token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        return payload
        
    except JWTError as e:
        logger.warning("Invalid JWT token", error=str(e))
        return None
    except Exception as e:
        logger.error("Failed to decode JWT", error=str(e))
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        User ID if valid token, None otherwise
    """
    payload = decode_jwt(token)
    
    if not payload:
        return None
    
    # Try common JWT claim names for user ID
    user_id = (
        payload.get('sub') or
        payload.get('user_id') or
        payload.get('cognito:username') or
        payload.get('username')
    )
    
    return user_id


def validate_token(token: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Validate JWT token and extract user ID.
    
    Args:
        token: JWT token string
        
    Returns:
        Tuple of (is_valid, user_id, error_message)
    """
    if not token:
        return False, None, "No token provided"
    
    user_id = get_user_id_from_token(token)
    
    if not user_id:
        return False, None, "Invalid token or missing user ID"
    
    return True, user_id, None