"""
Scanner execution engine.
Executes security scanners and collects results.
"""
from typing import List

from src.models.models_scan_result import ToolResult
from src.scanners.headers.scanners_headers import scan_headers
from src.scanners.tls.scanners_tls import scan_tls
from src.scanners.zap.scanners_zap import scan_zap
from src.scanners.nuclei.scanners_nuclei import scan_nuclei
from src.config.config_constants import ScanType
from src.utils.utils_logger import get_logger
from src.utils.value_normalizer import normalize_value


logger = get_logger(__name__)


class ScannerEngine:
    """Executes security scanners based on scan type."""
    
    def __init__(self, target: str, scan_type: ScanType):
        """
        Initialize scanner engine.
        
        Args:
            target: Target URL to scan
            scan_type: Type of scan to perform
        """
        self.target = target
        self.scan_type = scan_type
    
    def execute_scans(self) -> List[ToolResult]:
        """
        Execute all scanners for the specified scan type.
        
        Returns:
            List of tool results
        """
        logger.info(
            "Starting scan execution",
            target=self.target,
            scan_type = self.scan_type.value
        )
        
        results = []
        
        if self.scan_type == ScanType.QUICK:
            # Quick scan: Headers + TLS only
            results = self._execute_quick_scan()
        else:
            # Full scan: All tools
            results = self._execute_full_scan()
        
        logger.info(
            "Scan execution completed",
            target=self.target,
            tools_run=len(results)
        )
        
        return results
    
    def _execute_quick_scan(self) -> List[ToolResult]:
        """
        Execute quick scan (Headers + TLS).
        
        Returns:
            List of tool results
        """
        results = []
        
        # Headers scan
        logger.info("Executing headers scan")
        try:
            result = scan_headers(self.target)
            results.append(result)
        except Exception as e:
            logger.error("Headers scan failed", error=str(e))
        
        # TLS scan
        logger.info("Executing TLS scan")
        try:
            result = scan_tls(self.target)
            results.append(result)
        except Exception as e:
            logger.error("TLS scan failed", error=str(e))
        
        return results
    
    def _execute_full_scan(self) -> List[ToolResult]:
        """
        Execute full scan (Headers + TLS + ZAP + Nuclei).
        
        Returns:
            List of tool results
        """
        results = []
        
        # Start with quick scan tools
        results.extend(self._execute_quick_scan())
        
        # Add DAST tools
        
        # ZAP passive scan
        logger.info("Executing ZAP scan")
        try:
            result = scan_zap(self.target)
            results.append(result)
        except Exception as e:
            logger.error("ZAP scan failed", error=str(e))
        
        # Nuclei template scan
        logger.info("Executing Nuclei scan")
        try:
            result = scan_nuclei(self.target)
            results.append(result)
        except Exception as e:
            logger.error("Nuclei scan failed", error=str(e))
        
        return results


def execute_security_scans(target: str, scan_type: ScanType) -> List[ToolResult]:
    """
    Convenience function to execute security scans.
    
    Args:
        target: Target URL
        scan_type: Type of scan
        
    Returns:
        List of tool results
    """
    engine = ScannerEngine(target, scan_type)
    return engine.execute_scans()