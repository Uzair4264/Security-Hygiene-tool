"""
Repository pattern for data access.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.db.db_dynamodb import db_client
from src.models.models_scan_result import ScanResult
from src.config.config_constants import ScanStatus
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


class ScanRepository:
    """Repository for scan data operations."""
    
    @staticmethod
    def _build_pk(user_id: str) -> str:
        """Build partition key."""
        return f"USER#{user_id}"
    
    @staticmethod
    def _build_sk(scan_id: str) -> str:
        """Build sort key."""
        return f"SCAN#{scan_id}"
    
    @staticmethod
    def _build_gsi1_pk(status: str) -> str:
        """Build GSI1 partition key."""
        return f"STATUS#{status}"
    
    @staticmethod
    def _build_gsi1_sk(timestamp: str) -> str:
        """Build GSI1 sort key."""
        return f"CREATED#{timestamp}"
    
    def create_scan(
        self,
        scan_id: str,
        user_id: str,
        target: str,
        scan_type: str,
        environment: Optional[str] = None,
        github_repo: Optional[str] = None
    ) -> bool:
        """
        Create a new scan record.
        
        Args:
            scan_id: Unique scan identifier
            user_id: User identifier
            target: Target URL
            scan_type: Type of scan
            environment: Optional environment
            github_repo: Optional GitHub repository
            
        Returns:
            True if successful
        """
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'PK': self._build_pk(user_id),
            'SK': self._build_sk(scan_id),
            'GSI1PK': self._build_gsi1_pk(ScanStatus.PENDING.value),
            'GSI1SK': self._build_gsi1_sk(timestamp),
            'scan_id': scan_id,
            'user_id': user_id,
            'target': target,
            'scan_type': scan_type,
            'status': ScanStatus.PENDING.value,
            'created_at': timestamp,
            'tool_results': [],
        }
        
        if environment:
            item['environment'] = environment
        
        if github_repo:
            item['github_repo'] = github_repo
        
        try:
            db_client.put_item(item)
            logger.info("Scan created", scan_id=scan_id, user_id=user_id)
            return True
        except Exception as e:
            logger.error("Failed to create scan", scan_id=scan_id, error=str(e))
            raise
    
    def get_scan(self, user_id: str, scan_id: str) -> Optional[Dict[str, Any]]:
        """
        Get scan by ID.
        
        Args:
            user_id: User identifier
            scan_id: Scan identifier
            
        Returns:
            Scan data if found
        """
        pk = self._build_pk(user_id)
        sk = self._build_sk(scan_id)
        
        return db_client.get_item(pk, sk)
    
    def update_scan_status(
        self,
        user_id: str,
        scan_id: str,
        status: ScanStatus,
        error: Optional[str] = None
    ) -> bool:
        """
        Update scan status.
        
        Args:
            user_id: User identifier
            scan_id: Scan identifier
            status: New status
            error: Optional error message
            
        Returns:
            True if successful
        """
        pk = self._build_pk(user_id)
        sk = self._build_sk(scan_id)
        
        updates = {
            'status': status.value,
        }
        
        if status == ScanStatus.RUNNING:
            updates['started_at'] = datetime.utcnow().isoformat()
        elif status in [ScanStatus.COMPLETED, ScanStatus.FAILED]:
            updates['completed_at'] = datetime.utcnow().isoformat()
        
        if error:
            updates['error'] = error
        
        try:
            db_client.update_item(pk, sk, updates)
            logger.info("Scan status updated", scan_id=scan_id, status=status.value)
            return True
        except Exception as e:
            logger.error("Failed to update scan status", scan_id=scan_id, error=str(e))
            raise
    
    def update_scan_results(
        self,
        user_id: str,
        scan_id: str,
        tool_results: List[Dict[str, Any]],
        score: Dict[str, Any]
    ) -> bool:
        """
        Update scan with results.
        
        Args:
            user_id: User identifier
            scan_id: Scan identifier
            tool_results: Results from security tools
            score: Security score data
            
        Returns:
            True if successful
        """
        pk = self._build_pk(user_id)
        sk = self._build_sk(scan_id)
        
        updates = {
            'tool_results': tool_results,
            'score': score,
            'status': ScanStatus.COMPLETED.value,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        try:
            db_client.update_item(pk, sk, updates)
            logger.info("Scan results updated", scan_id=scan_id)
            return True
        except Exception as e:
            logger.error("Failed to update scan results", scan_id=scan_id, error=str(e))
            raise
    
    def get_user_scans(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get all scans for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of results
            
        Returns:
            List of scan records
        """
        pk = self._build_pk(user_id)
        
        return db_client.query(pk, limit=limit)


# Global instance
scan_repository = ScanRepository()