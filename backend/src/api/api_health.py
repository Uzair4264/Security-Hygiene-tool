"""
Health check endpoint.
"""
from typing import Dict, Any

from src.utils.utils_response import success_response
from src.config.config_settings import settings
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Health check endpoint handler.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API response
    """
    logger.info("Health check requested")
    
    health_data = {
        "status": "healthy",
        "service": "zentrion-backend",
        "version": "1.0.0",
        "stage": settings.STAGE
    }
    
    return success_response(health_data)