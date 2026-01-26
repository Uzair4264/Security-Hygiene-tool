"""
Main application module for local testing and development.

This module provides a way to test Lambda handlers locally without deploying.
"""
import json
from typing import Dict, Any

from src.api.api_health import handler as health_handler
from src.api.scan.start_scan import handler as start_scan_handler
from src.api.scan.get_status import handler as get_status_handler
from src.api.scan.get_result import handler as get_result_handler
from src.core.core_orchestrator import handler as orchestrator_handler
from src.utils.utils_logger import get_logger


logger = get_logger(__name__)


class LocalTesting:
    """Helper class for local testing of Lambda handlers."""
    
    @staticmethod
    def test_health():
        """Test health check endpoint."""
        event = {
            'httpMethod': 'GET',
            'path': '/health'
        }
        response = health_handler(event, None)
        print("Health Check Response:")
        print(json.dumps(response, indent=2))
    
    @staticmethod
    def test_start_scan(target: str = "https://example.com", scan_type: str = "quick"):
        """Test start scan endpoint."""
        event = {
            'httpMethod': 'POST',
            'path': '/scan/start',
            'body': json.dumps({
                'target': target,
                'scan_type': scan_type
            }),
            'requestContext': {
                'authorizer': {
                    'user_id': 'test-user-123'
                }
            }
        }
        response = start_scan_handler(event, None)
        print("Start Scan Response:")
        print(json.dumps(response, indent=2))
        
        # Extract scan_id for further testing
        body = json.loads(response['body'])
        return body.get('data', {}).get('scan_id')
    
    @staticmethod
    def test_get_status(scan_id: str):
        """Test get scan status endpoint."""
        event = {
            'httpMethod': 'GET',
            'path': f'/scan/{scan_id}/status',
            'pathParameters': {
                'scan_id': scan_id
            },
            'requestContext': {
                'authorizer': {
                    'user_id': 'test-user-123'
                }
            }
        }
        response = get_status_handler(event, None)
        print("Get Status Response:")
        print(json.dumps(response, indent=2))
    
    @staticmethod
    def test_process_scan(scan_id: str, target: str = "https://example.com", scan_type: str = "quick"):
        """Test scan orchestrator."""
        event = {
            'scan_id': scan_id,
            'user_id': 'test-user-123',
            'target': target,
            'scan_type': scan_type
        }
        response = orchestrator_handler(event, None)
        print("Process Scan Response:")
        print(json.dumps(response, indent=2))


def main():
    """Main function for local testing."""
    print("=" * 60)
    print("Local Testing")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint...")
    LocalTesting.test_health()
    
    # Test start scan
    print("\n2. Testing Start Scan...")
    scan_id = LocalTesting.test_start_scan()
    
    if scan_id:
        # Test get status
        print("\n3. Testing Get Status...")
        LocalTesting.test_get_status(scan_id)
        
        # Test scan processor
        print("\n4. Testing Scan Processor...")
        LocalTesting.test_process_scan(scan_id)
        
        # Get final status
        print("\n5. Getting Final Status...")
        LocalTesting.test_get_status(scan_id)
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()