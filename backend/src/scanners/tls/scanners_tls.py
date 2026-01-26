"""
TLS/SSL configuration scanner.
"""
import time
import ssl
import socket
from typing import List
from urllib.parse import urlparse
from src.utils.value_normalizer import normalize_value
from src.models.models_scan_result import Issue, ToolResult
from src.config.config_constants import (
    MIN_TLS_VERSION,
    Severity,
    ScanCategory,
    TOOL_TLS
)
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


class TLSScanner:
    """Scanner for TLS/SSL configuration."""
    
    def __init__(self, target: str):
        """
        Initialize TLS scanner.
        
        Args:
            target: Target URL to scan
        """
        self.target = target
        parsed = urlparse(target)
        self.hostname = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    
    def scan(self) -> ToolResult:
        """
        Execute TLS security scan.
        
        Returns:
            Tool result with findings
        """
        start_time = time.time()
        
        try:
            logger.info("Starting TLS scan", target=self.target, hostname=self.hostname)
            
            # Skip if not HTTPS
            if not self.target.startswith('https://'):
                logger.info("Skipping TLS scan for non-HTTPS target")
                return ToolResult(
                    tool=TOOL_TLS,
                    category=ScanCategory.TLS,
                    severity={"critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0},
                    issues=[
                        Issue(
                            name="HTTPS not enabled",
                            description="The target does not use HTTPS encryption",
                            severity=Severity.CRITICAL,
                            category=ScanCategory.TLS,
                            owasp="A02:2021 – Cryptographic Failures",
                            recommendation="Enable HTTPS with a valid TLS certificate",
                            evidence=f"Target URL uses {urlparse(self.target).scheme}://"
                        )
                    ],
                    execution_time=time.time() - start_time,
                    status="success"
                )
            
            issues = self._analyze_tls()
            
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
                "TLS scan completed",
                target=self.target,
                issues_found=len(issues),
                execution_time=execution_time
            )
            
            return ToolResult(
                tool=TOOL_TLS,
                category=ScanCategory.TLS,
                severity=severity_count,
                issues=issues,
                execution_time=execution_time,
                status="success"
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("TLS scan failed", target=self.target, error=str(e))
            
            return ToolResult(
                tool=TOOL_TLS,
                category=ScanCategory.TLS,
                severity={"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
                issues=[],
                execution_time=execution_time,
                status="failed",
                error=str(e)
            )
    
    def _analyze_tls(self) -> List[Issue]:
        """
        Analyze TLS configuration.
        
        Returns:
            List of security issues
        """
        issues = []
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect and get certificate
            with socket.create_connection((self.hostname, self.port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    # Check TLS version
                    issues.extend(self._check_tls_version(version))
                    
                    # Check cipher suite
                    issues.extend(self._check_cipher(cipher))
                    
                    # Check certificate
                    issues.extend(self._check_certificate(cert))
            
        except ssl.SSLError as e:
            issues.append(Issue(
                name="SSL/TLS connection error",
                description=f"Failed to establish secure connection: {str(e)}",
                severity=Severity.HIGH,
                category=ScanCategory.TLS,
                owasp="A02:2021 – Cryptographic Failures",
                recommendation="Verify TLS configuration and certificate validity",
                evidence=str(e)
            ))
        except Exception as e:
            logger.warning("TLS analysis error", error=str(e))
        
        return issues
    
    def _check_tls_version(self, version: str) -> List[Issue]:
        """Check TLS version security."""
        issues = []
        
        # Map version strings to numeric comparison
        version_order = {
            "SSLv2": 0,
            "SSLv3": 1,
            "TLSv1": 2,
            "TLSv1.1": 3,
            "TLSv1.2": 4,
            "TLSv1.3": 5
        }
        
        current_version = version_order.get(version, 0)
        min_version = version_order.get(MIN_TLS_VERSION, 4)
        
        if current_version < min_version:
            issues.append(Issue(
                name="Outdated TLS version",
                description=f"Server is using {version}, which is outdated",
                severity=Severity.HIGH,
                category=ScanCategory.TLS,
                owasp="A02:2021 – Cryptographic Failures",
                recommendation=f"Upgrade to {MIN_TLS_VERSION} or higher",
                evidence=f"Current version: {version}"
            ))
        
        return issues
    
    def _check_cipher(self, cipher: tuple) -> List[Issue]:
        """Check cipher suite security."""
        issues = []
        
        if not cipher:
            return issues
        
        cipher_name = cipher[0]
        
        # Check for weak ciphers
        weak_indicators = ['DES', 'RC4', 'MD5', 'NULL', 'EXPORT', 'anon']
        
        for indicator in weak_indicators:
            if indicator in cipher_name.upper():
                issues.append(Issue(
                    name="Weak cipher suite detected",
                    description=f"The cipher suite {cipher_name} contains weak cryptography",
                    severity=Severity.HIGH,
                    category=ScanCategory.TLS,
                    owasp="A02:2021 – Cryptographic Failures",
                    recommendation="Use strong cipher suites (AES-GCM, ChaCha20)",
                    evidence=f"Cipher: {cipher_name}"
                ))
                break
        
        return issues
    
    def _check_certificate(self, cert: dict) -> List[Issue]:
        """Check certificate configuration."""
        issues = []
        
        # Certificate validation is handled by SSL context
        # Additional checks can be added here
        
        return issues


def scan_tls(target: str) -> ToolResult:
    """
    Convenience function to scan TLS.
    
    Args:
        target: Target URL
        
    Returns:
        Tool result
    """
    scanner = TLSScanner(target)
    return scanner.scan()