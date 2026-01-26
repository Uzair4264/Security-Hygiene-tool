"""
Configuration settings for Zentrion backend.
Loads from environment variables with sensible defaults.
"""
import os
from typing import Optional


class Settings:
    """Application settings loaded from environment."""
    IS_LOCAL = os.getenv("LOCAL_MODE", "false").lower() == "true"
    # AWS
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "zentrion-dev-scans")
    
    # Stage
    STAGE: str = os.getenv("STAGE", "dev")
    
    # Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-in-prod")
    JWT_ALGORITHM: str = "HS256"
    ALLOW_ANONYMOUS: bool = os.getenv("ALLOW_ANONYMOUS", "false").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Scan Configuration
    SCAN_TIMEOUT_SECONDS: int = int(os.getenv("SCAN_TIMEOUT_SECONDS", "600"))
    MAX_CONCURRENT_SCANS: int = int(os.getenv("MAX_CONCURRENT_SCANS", "5"))
    
    # Lambda
    LAMBDA_FUNCTION_NAME_SCAN_PROCESSOR: str = os.getenv(
        "LAMBDA_FUNCTION_NAME_SCAN_PROCESSOR",
        f"zentrion-backend-{STAGE}-processScan"
    )
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode."""
        return cls.STAGE in ["dev", "local"]
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode."""
        return cls.STAGE == "prod"


settings = Settings()