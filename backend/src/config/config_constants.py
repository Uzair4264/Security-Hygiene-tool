"""
Constants used throughout the application.
"""
from enum import Enum


class ScanStatus(str, Enum):
    """Scan execution status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ScanType(str, Enum):
    """Types of security scans."""
    QUICK = "quick"
    FULL = "full"


class Environment(str, Enum):
    """Target environment types."""
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


class Severity(str, Enum):
    """Issue severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanCategory(str, Enum):
    """Security scan categories."""
    HEADERS = "headers"
    TLS = "tls"
    COOKIES = "cookies"
    DAST = "dast"
    SAST = "sast"


# Scoring weights
SEVERITY_WEIGHTS = {
    Severity.CRITICAL: -25,
    Severity.HIGH: -15,
    Severity.MEDIUM: -7,
    Severity.LOW: -3,
    Severity.INFO: 0,
}

# Score grading
SCORE_GRADES = [
    (90, "A", "Excellent security posture"),
    (80, "B", "Good security with minor issues"),
    (70, "C", "Moderate security issues detected"),
    (60, "D", "Significant security concerns"),
    (0, "F", "Critical security vulnerabilities"),
]

# DynamoDB key patterns
PK_USER = "USER#{user_id}"
SK_SCAN = "SCAN#{scan_id}"
GSI1PK_STATUS = "STATUS#{status}"
GSI1SK_CREATED = "CREATED#{timestamp}"

# Tool names
TOOL_HEADERS = "headers"
TOOL_TLS = "tls"
TOOL_ZAP = "zap"
TOOL_NUCLEI = "nuclei"

# HTTP Headers to check
REQUIRED_SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
]

# TLS minimum version
MIN_TLS_VERSION = "TLSv1.2"