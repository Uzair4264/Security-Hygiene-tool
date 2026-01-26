"""
Manually trigger scan processing for local testing.
Run this after starting a scan to process it.
"""
import sys
import os

# Set local mode BEFORE any other imports
os.environ['LOCAL_MODE'] = 'true'
os.environ['ALLOW_ANONYMOUS'] = 'true'
os.environ['JWT_SECRET'] = 'local-dev-secret'
os.environ['DYNAMODB_TABLE'] = 'local-test-table'

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.core_orchestrator import ScanOrchestrator


def process_scan(scan_id: str, target: str = "http://testphp.vulnweb.com", scan_type: str = "quick"):
    """Process a scan locally."""
    print("\n" + "=" * 60)
    print("🔍 Processing Scan")
    print("=" * 60)
    print(f"Scan ID:    {scan_id}")
    print(f"Target:     {target}")
    print(f"Scan Type:  {scan_type}")
    print("=" * 60 + "\n")
    
    orchestrator = ScanOrchestrator(
        scan_id=scan_id,
        user_id='local-test-user',
        target=target,
        scan_type=scan_type
    )
    
    try:
        success = orchestrator.execute()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ Scan Processing: SUCCESS")
            print("=" * 60)
            print(f"\n📊 View results at:")
            print(f"   http://localhost:5000/scan/{scan_id}/result")
            print(f"\n📈 Or check status:")
            print(f"   http://localhost:5000/scan/{scan_id}/status")
        else:
            print("❌ Scan Processing: FAILED")
            print("=" * 60)
            print("\nCheck the logs above for error details")
        print()
        
        return success
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Scan Processing: ERROR")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n" + "=" * 60)
        print("❌ Usage Error")
        print("=" * 60)
        print("\nUsage: python run_scan.py <scan_id> [target] [scan_type]")
        print("\nExamples:")
        print("  python run_scan.py abc-123-def")
        print("  python run_scan.py abc-123-def https://example.com")
        print("  python run_scan.py abc-123-def https://example.com full")
        print("\n" + "=" * 60 + "\n")
        sys.exit(1)
    
    scan_id = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "https://example.com"
    scan_type = sys.argv[3] if len(sys.argv) > 3 else "quick"
    
    process_scan(scan_id, target, scan_type)