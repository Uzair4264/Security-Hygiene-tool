"""
Nuclei vulnerability scanner simulation.

NOTE: This is a design abstraction. In production, this would:
1. Run Nuclei binary in Lambda via layers or container
2. Execute: nuclei -u <target> -j -o results.json
3. Parse JSON output
4. Normalize findings

This implementation provides realistic mock findings for demonstration.
"""
import time
from typing import List

from src.models.models_scan_result import Issue, ToolResult
from src.config.config_constants import Severity, ScanCategory, TOOL_NUCLEI
from src.utils.utils_logger import get_logger
from src.utils.value_normalizer import normalize_value


logger = get_logger(__name__)


class NucleiScanner:
    """Nuclei template-based scanner abstraction."""
    
    # Simulated Nuclei template findings
    TEMPLATE_FINDINGS = [
        {
            "template_id": "exposed-panels",
            "name": "Exposed Administration Panel",
            "severity": Severity.HIGH,
            "description": "An administrative panel is accessible without authentication",
            "recommendation": "Restrict access to admin panels using IP whitelisting or authentication",
            "cwe": "CWE-425",
            "owasp": "A01:2021 – Broken Access Control"
        },
        {
            "template_id": "default-credentials",
            "name": "Default Credentials Detected",
            "severity": Severity.CRITICAL,
            "description": "Default credentials are in use on the application",
            "recommendation": "Change all default credentials immediately",
            "cwe": "CWE-798",
            "owasp": "A07:2021 – Identification and Authentication Failures"
        },
        {
            "template_id": "exposed-git",
            "name": "Exposed .git Directory",
            "severity": Severity.HIGH,
            "description": "The .git directory is publicly accessible",
            "recommendation": "Block access to .git directory in web server configuration",
            "cwe": "CWE-538",
            "owasp": "A05:2021 – Security Misconfiguration"
        },
        {
            "template_id": "tech-detect",
            "name": "Technology Detection",
            "severity": Severity.INFO,
            "description": "Server technology and framework versions detected",
            "recommendation": "Consider obscuring version information",
            "cwe": "CWE-200",
            "owasp": "A05:2021 – Security Misconfiguration"
        },
    ]
    
    def __init__(self, target: str):
        """
        Initialize Nuclei scanner.
        
        Args:
            target: Target URL to scan
        """
        self.target = target
    
    def scan(self) -> ToolResult:
        """
        Execute Nuclei template scan.
        
        Returns:
            Tool result with findings
        """
        start_time = time.time()
        
        try:
            logger.info("Starting Nuclei scan", target=self.target)
            
            # Simulate Nuclei scan execution
            # In production: subprocess.run(['nuclei', '-u', target, '-j'])
            issues = self._simulate_nuclei_scan()
            
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
                "Nuclei scan completed",
                target=self.target,
                issues_found=len(issues),
                execution_time=execution_time
            )
            
            return ToolResult(
                tool=TOOL_NUCLEI,
                category=ScanCategory.DAST,
                severity=severity_count,
                issues=issues,
                execution_time=execution_time,
                status="success"
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("Nuclei scan failed", target=self.target, error=str(e))
            
            return ToolResult(
                tool=TOOL_NUCLEI,
                category=ScanCategory.DAST,
                severity={"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
                issues=[],
                execution_time=execution_time,
                status="failed",
                error=str(e)
            )
    
    def _simulate_nuclei_scan(self) -> List[Issue]:
        """
        Simulate Nuclei template execution.
        
        In production, this would:
        1. Execute nuclei binary
        2. Parse JSON output
        3. Map to Issue model
        
        Returns:
            List of issues
        """
        issues = []
        
        # Simulate finding 1-2 issues randomly
        # In real implementation, this would be based on actual scan results
        import random
        num_findings = random.randint(0, 2)
        
        for i in range(num_findings):
            finding = self.TEMPLATE_FINDINGS[i]
            issues.append(Issue(
                name=finding["name"],
                description=finding["description"],
                severity=finding["severity"],
                category=ScanCategory.DAST,
                cwe=finding["cwe"],
                owasp=finding["owasp"],
                recommendation=finding["recommendation"],
                evidence=f"Matched template: {finding['template_id']}"
            ))
        
        # Always include tech detection
        tech_finding = self.TEMPLATE_FINDINGS[3]
        issues.append(Issue(
            name=tech_finding["name"],
            description=tech_finding["description"],
            severity=tech_finding["severity"],
            category=ScanCategory.DAST,
            cwe=tech_finding["cwe"],
            owasp=tech_finding["owasp"],
            recommendation=tech_finding["recommendation"],
            evidence="Multiple technologies detected via fingerprinting"
        ))
        
        return issues


def scan_nuclei(target: str) -> ToolResult:
    """
    Convenience function to scan with Nuclei.
    
    Args:
        target: Target URL
        
    Returns:
        Tool result
    """
    scanner = NucleiScanner(target)
    return scanner.scan()