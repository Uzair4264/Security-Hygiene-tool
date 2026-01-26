"""
Pydantic models for scan results.
"""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from src.config.config_constants import ScanStatus, Severity, ScanCategory


class Issue(BaseModel):
    """Individual security issue found during scan."""
    
    name: str = Field(..., description="Issue name")
    description: str = Field(..., description="Issue description")
    severity: Severity = Field(..., description="Issue severity")
    category: ScanCategory = Field(..., description="Issue category")
    cwe: Optional[str] = Field(None, description="CWE identifier")
    owasp: Optional[str] = Field(None, description="OWASP reference")
    recommendation: str = Field(..., description="Fix recommendation")
    evidence: Optional[str] = Field(None, description="Evidence or example")
    
    class Config:
        """Pydantic config."""
        use_enum_values = True


class ToolResult(BaseModel):
    """Result from a single security tool."""
    
    tool: str = Field(..., description="Tool name")
    category: ScanCategory = Field(..., description="Scan category")
    severity: Dict[str, int] = Field(
        default_factory=lambda: {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        },
        description="Count of issues by severity"
    )
    issues: List[Issue] = Field(default_factory=list, description="List of issues found")
    execution_time: float = Field(..., description="Tool execution time in seconds")
    status: str = Field(default="success", description="Tool execution status")
    error: Optional[str] = Field(None, description="Error message if failed")
    
    class Config:
        """Pydantic config."""
        use_enum_values = True


class SecurityScore(BaseModel):
    """Security hygiene score details."""
    
    score: int = Field(..., ge=0, le=100, description="Security score (0-100)")
    grade: str = Field(..., description="Letter grade (A-F)")
    summary: str = Field(..., description="Score summary")
    
    total_issues: int = Field(default=0, description="Total issues found")
    critical_count: int = Field(default=0, description="Critical issues")
    high_count: int = Field(default=0, description="High severity issues")
    medium_count: int = Field(default=0, description="Medium severity issues")
    low_count: int = Field(default=0, description="Low severity issues")
    
    breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="Score breakdown by category"
    )


class ScanResult(BaseModel):
    """Complete scan result."""
    
    scan_id: str = Field(..., description="Unique scan identifier")
    user_id: str = Field(..., description="User who initiated the scan")
    target: str = Field(..., description="Target URL")
    scan_type: str = Field(..., description="Type of scan performed")
    environment: Optional[str] = Field(None, description="Target environment")
    
    status: ScanStatus = Field(..., description="Scan status")
    
    tool_results: List[ToolResult] = Field(
        default_factory=list,
        description="Results from security tools"
    )
    
    score: Optional[SecurityScore] = Field(None, description="Security score")
    
    created_at: str = Field(..., description="Scan creation timestamp")
    started_at: Optional[str] = Field(None, description="Scan start timestamp")
    completed_at: Optional[str] = Field(None, description="Scan completion timestamp")
    
    error: Optional[str] = Field(None, description="Error message if failed")
    
    class Config:
        """Pydantic config."""
        use_enum_values = True