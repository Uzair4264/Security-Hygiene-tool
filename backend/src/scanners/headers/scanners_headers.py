"""
HTTP Security Headers scanner.
"""
import time
from typing import Dict, List
import requests
from src.models.models_scan_result import Issue, ToolResult
from src.utils.value_normalizer import normalize_value
from src.config.config_constants import (
    REQUIRED_SECURITY_HEADERS,
    Severity,
    ScanCategory,
    TOOL_HEADERS
)
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


class HeadersScanner:
    """Scanner for HTTP security headers."""
    
    HEADER_INFO = {
        "Strict-Transport-Security": {
            "description": "Enforces HTTPS connections",
            "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains",
            "severity": Severity.HIGH,
            "owasp": "A05:2021 – Security Misconfiguration"
        },
        "X-Content-Type-Options": {
            "description": "Prevents MIME type sniffing",
            "recommendation": "Add: X-Content-Type-Options: nosniff",
            "severity": Severity.MEDIUM,
            "owasp": "A05:2021 – Security Misconfiguration"
        },
        "X-Frame-Options": {
            "description": "Prevents clickjacking attacks",
            "recommendation": "Add: X-Frame-Options: DENY or SAMEORIGIN",
            "severity": Severity.MEDIUM,
            "owasp": "A04:2021 – Insecure Design"
        },
        "Content-Security-Policy": {
            "description": "Controls resource loading and prevents XSS",
            "recommendation": "Add a strict Content-Security-Policy header",
            "severity": Severity.HIGH,
            "owasp": "A03:2021 – Injection"
        },
        "X-XSS-Protection": {
            "description": "Legacy XSS protection (deprecated but still useful)",
            "recommendation": "Add: X-XSS-Protection: 1; mode=block",
            "severity": Severity.LOW,
            "owasp": "A03:2021 – Injection"
        },
        "Referrer-Policy": {
            "description": "Controls referrer information leakage",
            "recommendation": "Add: Referrer-Policy: strict-origin-when-cross-origin",
            "severity": Severity.LOW,
            "owasp": "A05:2021 – Security Misconfiguration"
        },
        "Permissions-Policy": {
            "description": "Controls browser features and APIs",
            "recommendation": "Add: Permissions-Policy: geolocation=(), microphone=(), camera=()",
            "severity": Severity.LOW,
            "owasp": "A05:2021 – Security Misconfiguration"
        },
    }
    
    def __init__(self, target: str):
        """
        Initialize headers scanner.
        
        Args:
            target: Target URL to scan
        """
        self.target = target
    
    def scan(self) -> ToolResult:
        """
        Execute headers security scan.
        
        Returns:
            Tool result with findings
        """
        start_time = time.time()
        
        try:
            logger.info("Starting headers scan", target=self.target)
            
            # Fetch headers
            response = requests.get(
                self.target,
                timeout=10,
                allow_redirects=True,
                verify=True
            )
            
            headers = response.headers
            issues = self._analyze_headers(headers)
            
            # Count severity
            severity_count = {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0
            }
            
            for issue in issues:
                key = issue.severity.lower() if isinstance(issue.severity, str) else issue.severity.value
                severity_count[key] += 1
            
            execution_time = time.time() - start_time
            
            logger.info(
                "Headers scan completed",
                target=self.target,
                issues_found=len(issues),
                execution_time=execution_time
            )
            
            return ToolResult(
                tool=TOOL_HEADERS,
                category=ScanCategory.HEADERS,
                severity=severity_count,
                issues=issues,
                execution_time=execution_time,
                status="success"
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("Headers scan failed", target=self.target, error=str(e))
            
            return ToolResult(
                tool=TOOL_HEADERS,
                category=ScanCategory.HEADERS,
                severity={"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
                issues=[],
                execution_time=execution_time,
                status="failed",
                error=str(e)
            )
    
    def _analyze_headers(self, headers: Dict) -> List[Issue]:
        """
        Analyze HTTP headers for security issues.
        
        Args:
            headers: Response headers
            
        Returns:
            List of security issues
        """
        issues = []
        
        # Check for missing security headers
        for header_name in REQUIRED_SECURITY_HEADERS:
            if header_name not in headers:
                info = self.HEADER_INFO.get(header_name, {})
                
                issues.append(Issue(
                    name=f"Missing {header_name} header",
                    description=info.get("description", f"The {header_name} header is not set"),
                    severity=info.get("severity", Severity.MEDIUM),
                    category=ScanCategory.HEADERS,
                    owasp=info.get("owasp"),
                    recommendation=info.get("recommendation", f"Add the {header_name} header"),
                    evidence=f"Header '{header_name}' not found in response"
                ))
        
        # Check for insecure header values
        issues.extend(self._check_header_values(headers))
        
        return issues
    
    def _check_header_values(self, headers: Dict) -> List[Issue]:
        """Check for insecure header values."""
        issues = []
        
        # Check X-Frame-Options
        if "X-Frame-Options" in headers:
            value = headers["X-Frame-Options"].upper()
            if value not in ["DENY", "SAMEORIGIN"]:
                issues.append(Issue(
                    name="Weak X-Frame-Options configuration",
                    description="X-Frame-Options should be set to DENY or SAMEORIGIN",
                    severity=Severity.MEDIUM,
                    category=ScanCategory.HEADERS,
                    owasp="A04:2021 – Insecure Design",
                    recommendation="Set X-Frame-Options to DENY or SAMEORIGIN",
                    evidence=f"Current value: {headers['X-Frame-Options']}"
                ))
        
        # Check for information disclosure headers
        disclosure_headers = ["Server", "X-Powered-By", "X-AspNet-Version"]
        for header in disclosure_headers:
            if header in headers:
                issues.append(Issue(
                    name=f"Information disclosure via {header} header",
                    description=f"The {header} header reveals server technology information",
                    severity=Severity.INFO,
                    category=ScanCategory.HEADERS,
                    owasp="A05:2021 – Security Misconfiguration",
                    recommendation=f"Remove or obfuscate the {header} header",
                    evidence=f"{header}: {headers[header]}"
                ))
        
        return issues


def scan_headers(target: str) -> ToolResult:
    """
    Convenience function to scan headers.
    
    Args:
        target: Target URL
        
    Returns:
        Tool result
    """
    scanner = HeadersScanner(target)
    return scanner.scan()