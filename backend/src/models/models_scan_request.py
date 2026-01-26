"""
Pydantic models for scan requests.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.config.config_constants import ScanType, Environment


class ScanRequest(BaseModel):
    """Request model for starting a scan."""
    
    target: str = Field(
        ...,
        description="Target URL to scan",
        example="https://example.com"
    )
    
    scan_type: ScanType = Field(
        default=ScanType.QUICK,
        description="Type of scan to perform"
    )
    
    environment: Optional[Environment] = Field(
        default=None,
        description="Target environment type"
    )
    
    github_repo: Optional[str] = Field(
        default=None,
        description="GitHub repository URL for SAST scanning"
    )
    
    @field_validator('target')
    @classmethod
    def validate_target_url(cls, v: str) -> str:
        """Validate and normalize target URL."""
        if not v:
            raise ValueError("Target URL is required")
        
        # Ensure URL has a scheme
        if not v.startswith(('http://', 'https://')):
            v = f'https://{v}'
        
        return v.strip()
