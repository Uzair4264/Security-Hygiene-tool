"""
OWASP ZAP passive scanner simulation.

NOTE: This is a design abstraction. In production, this would:
1. Run ZAP in a Docker container
2. Use ZAP API to trigger passive scans
3. Parse ZAP XML/JSON reports
4. For Lambda, use ECS/Fargate to run ZAP containers

This implementation provides realistic mock findings for demonstration.
"""
import time
from typing import List
import requests

from src.models.models_scan_result import Issue, ToolResult
from src.config.config_constants import Severity, ScanCategory, TOOL_ZAP
from src.utils.utils_logger import get_logger
from src.utils.value_normalizer import normalize_value

logger = get_logger(__name__)


class ZAPScanner:
    """OWASP ZAP passive scanner abstraction."""
    
    # Simulated ZAP findings based on common vulnerabilities
    COMMON_ZAP_FINDINGS = [
        {
            "name": "Cookie without Secure flag",
            "severity": Severity.MEDIUM,
            "description": "A cookie has been set without the secure flag",
            "recommendation": "Set the 'Secure' flag on all cookies",
            "cwe": "CWE-614",
            "owasp": "A05:2021 – Security Misconfiguration"
        },
        {
            "name": "Cookie without HttpOnly flag",
            "severity": Severity.MEDIUM,
            "description": "A cookie has been set without the HttpOnly flag",
            "recommendation": "Set the 'HttpOnly' flag on all cookies to prevent XSS",
            "cwe": "CWE-1004",
            "owasp": "A03:2021 – Injection"
        },
        {
            "name": "Cross-Domain JavaScript source file inclusion",
            "severity": Severity.LOW,
            "description": "The page includes JavaScript from external domains",
            "recommendation": "Use Subresource Integrity (SRI) for external scripts",
            "cwe": "CWE-829",
            "owasp": "A08:2021 – Software and Data Integrity Failures"
        },
        {
            "name": "Incomplete or missing charset declaration",
            "severity": Severity.INFO,
            "description": "The page does not specify a character encoding",
            "recommendation": "Specify charset in Content-Type header or meta tag",
            "cwe": "CWE-172",
            "owasp": "A05:2021 – Security Misconfiguration"
        },
    ]
    
    def __init__(self, target: str):
        """
        Initialize ZAP scanner.
        
        Args:
            target: Target URL to scan
        """
        self.target = target
    
    def scan(self) -> ToolResult:
        """
        Execute ZAP passive scan.
        
        Returns:
            Tool result with findings
        """
        start_time = time.time()
        
        try:
            logger.info("Starting ZAP passive scan", target=self.target)
            
            # Fetch target to analyze (passive scan would analyze all traffic)
            response = requests.get(self.target, timeout=10, verify=True)
            
            # Simulate passive scan analysis
            issues = self._simulate_passive_scan(response)
            
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
                "ZAP scan completed",
                target=self.target,
                issues_found=len(issues),
                execution_time=execution_time
            )
            
            return ToolResult(
                tool=TOOL_ZAP,
                category=ScanCategory.DAST,
                severity=severity_count,
                issues=issues,
                execution_time=execution_time,
                status="success"
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("ZAP scan failed", target=self.target, error=str(e))
            
            return ToolResult(
                tool=TOOL_ZAP,
                category=ScanCategory.DAST,
                severity={"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
                issues=[],
                execution_time=execution_time,
                status="failed",
                error=str(e)
            )
    
    def _simulate_passive_scan(self, response) -> List[Issue]:
        """
        Simulate ZAP passive scan findings.
        
        In production, this would:
        1. Start ZAP daemon
        2. Proxy traffic through ZAP
        3. Fetch passive scan results via API
        4. Parse and normalize findings
        
        Args:
            response: HTTP response to analyze
            
        Returns:
            List of issues
        """
        issues = []
        
        # Analyze cookies
        if 'Set-Cookie' in response.headers:
            cookies = response.headers.get('Set-Cookie', '')
            
            if 'Secure' not in cookies:
                finding = self.COMMON_ZAP_FINDINGS[0]
                issues.append(Issue(
                    name=finding["name"],
                    description=finding["description"],
                    severity=finding["severity"],
                    category=ScanCategory.COOKIES,
                    cwe=finding["cwe"],
                    owasp=finding["owasp"],
                    recommendation=finding["recommendation"],
                    evidence=f"Cookie found without Secure flag"
                ))
            
            if 'HttpOnly' not in cookies:
                finding = self.COMMON_ZAP_FINDINGS[1]
                issues.append(Issue(
                    name=finding["name"],
                    description=finding["description"],
                    severity=finding["severity"],
                    category=ScanCategory.COOKIES,
                    cwe=finding["cwe"],
                    owasp=finding["owasp"],
                    recommendation=finding["recommendation"],
                    evidence=f"Cookie found without HttpOnly flag"
                ))
        
        # Analyze content
        content = response.text
        
        # Check for external scripts
        if '<script src="http' in content:
            finding = self.COMMON_ZAP_FINDINGS[2]
            issues.append(Issue(
                name=finding["name"],
                description=finding["description"],
                severity=finding["severity"],
                category=ScanCategory.DAST,
                cwe=finding["cwe"],
                owasp=finding["owasp"],
                recommendation=finding["recommendation"],
                evidence="External JavaScript sources detected"
            ))
        
        # Check charset
        if 'charset' not in response.headers.get('Content-Type', '').lower():
            if '<meta charset' not in content.lower():
                finding = self.COMMON_ZAP_FINDINGS[3]
                issues.append(Issue(
                    name=finding["name"],
                    description=finding["description"],
                    severity=finding["severity"],
                    category=ScanCategory.DAST,
                    cwe=finding["cwe"],
                    owasp=finding["owasp"],
                    recommendation=finding["recommendation"],
                    evidence="No charset declaration found"
                ))
        
        return issues


def scan_zap(target: str) -> ToolResult:
    """
    Convenience function to scan with ZAP.
    
    Args:
        target: Target URL
        
    Returns:
        Tool result
    """
    scanner = ZAPScanner(target)
    return scanner.scan()