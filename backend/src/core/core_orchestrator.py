"""
Scan orchestration logic.
Coordinates scanner execution and result processing.
"""
from typing import Dict, Any

from src.core.scanner_engine import execute_security_scans
from src.core.core_scoring import calculate_hygiene_score
from src.db.db_repositories import scan_repository
from src.config.config_constants import ScanStatus, ScanType
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


class ScanOrchestrator:
    """Orchestrates security scan execution."""
    
    def __init__(self, scan_id: str, user_id: str, target: str, scan_type: str):
        """
        Initialize scan orchestrator.
        
        Args:
            scan_id: Scan identifier
            user_id: User identifier
            target: Target URL
            scan_type: Type of scan
        """
        self.scan_id = scan_id
        self.user_id = user_id
        self.target = target
        self.scan_type = ScanType(scan_type)
    
    def execute(self) -> bool:
        """
        Execute the complete scan workflow.
        
        Returns:
            True if successful
        """
        try:
            logger.info(
                "Starting scan orchestration",
                scan_id=self.scan_id,
                target=self.target
            )
            
            # Update status to RUNNING
            scan_repository.update_scan_status(
                self.user_id,
                self.scan_id,
                ScanStatus.RUNNING
            )
            
            # Execute scanners
            tool_results = execute_security_scans(self.target, self.scan_type)
            
            # Calculate security score
            security_score = calculate_hygiene_score(tool_results)
            
            # Convert to dict for storage
            tool_results_dict = [result.model_dump() for result in tool_results]
            score_dict = security_score.model_dump()
            
            # Update scan with results
            scan_repository.update_scan_results(
                self.user_id,
                self.scan_id,
                tool_results_dict,
                score_dict
            )
            
            logger.info(
                "Scan orchestration completed successfully",
                scan_id=self.scan_id,
                score=security_score.score
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "Scan orchestration failed",
                scan_id=self.scan_id,
                error=str(e)
            )
            
            # Update status to FAILED
            scan_repository.update_scan_status(
                self.user_id,
                self.scan_id,
                ScanStatus.FAILED,
                error=str(e)
            )
            
            return False


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for scan processing.
    
    This Lambda is invoked asynchronously to process scans.
    
    Args:
        event: Lambda event containing scan details
        context: Lambda context
        
    Returns:
        Response dict
    """
    try:
        # Extract scan details from event
        scan_id = event.get('scan_id')
        user_id = event.get('user_id')
        target = event.get('target')
        scan_type = event.get('scan_type')
        
        logger.info(
            "Scan processor invoked",
            scan_id=scan_id,
            user_id=user_id
        )
        
        # Execute scan
        orchestrator = ScanOrchestrator(scan_id, user_id, target, scan_type)
        success = orchestrator.execute()
        
        return {
            'statusCode': 200 if success else 500,
            'body': {
                'scan_id': scan_id,
                'success': success
            }
        }
        
    except Exception as e:
        logger.error("Scan processor error", error=str(e))
        return {
            'statusCode': 500,
            'body': {
                'error': str(e)
            }
        }