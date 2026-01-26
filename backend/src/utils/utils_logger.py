"""
Structured logging utility for Lambda functions.
"""
import json
import logging
import sys
from typing import Any, Dict, Optional

from src.config.config_settings import settings


class StructuredLogger:
    """Structured JSON logger for cloud environments."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)
    
    def _log(self, level: str, message: str, **kwargs):
        """Log with structured JSON format."""
        log_entry = {
            "level": level,
            "message": message,
            "stage": settings.STAGE,
            **kwargs
        }
        
        log_method = getattr(self.logger, level.lower())
        log_method(json.dumps(log_entry))
    
    def info(self, message: str, **kwargs):
        """Log info level message."""
        self._log("INFO", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error level message."""
        self._log("ERROR", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message."""
        self._log("WARNING", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug level message."""
        self._log("DEBUG", message, **kwargs)


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance."""
    return StructuredLogger(name)