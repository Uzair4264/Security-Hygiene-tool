"""
Local development server for testing backend without AWS.
Simulates API Gateway by running Flask server.
Works with your current file naming convention.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Set local mode BEFORE any other imports
os.environ['LOCAL_MODE'] = 'true'
os.environ['ALLOW_ANONYMOUS'] = 'true'
os.environ['JWT_SECRET'] = 'local-dev-secret'
os.environ['DYNAMODB_TABLE'] = 'local-test-table'

print("=" * 60)
print("🔧 Environment Setup")
print("=" * 60)
print(f"LOCAL_MODE: {os.getenv('LOCAL_MODE')}")
print(f"ALLOW_ANONYMOUS: {os.getenv('ALLOW_ANONYMOUS')}")
print("=" * 60 + "\n")

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Import your Lambda handlers (using YOUR file naming)
try:
    from src.api.api_health import handler as health_handler
    from src.api.scan.start_scan import handler as start_scan_handler
    from src.api.scan.get_status import handler as get_status_handler
    from src.api.scan.get_result import handler as get_result_handler
    print("✅ All API handlers imported successfully\n")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please check your file names match:\n")
    print("  - src/api/api_health.py")
    print("  - src/api/scan/start_scan.py")
    print("  - src/api/scan/get_status.py")
    print("  - src/api/scan/get_result.py")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

print("🌐 CORS enabled for all origins")


def lambda_to_flask(handler_func, event):
    """Convert Lambda handler response to Flask response."""
    try:
        result = handler_func(event, None)
        
        # Extract body and status code
        status_code = result.get('statusCode', 200)
        body = result.get('body', '{}')
        
        # Parse JSON body
        try:
            response_data = json.loads(body)
        except:
            response_data = {'error': 'Invalid response'}
        
        return jsonify(response_data), status_code
    except Exception as e:
        print(f"❌ Handler error: {e}")
        return jsonify({
            'success': False,
            'error': {
                'message': str(e)
            }
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    print("📡 Health check requested")
    event = {
        'httpMethod': 'GET',
        'path': '/health'
    }
    return lambda_to_flask(health_handler, event)


@app.route('/scan/start', methods=['POST', 'OPTIONS'])
def start_scan():
    """Start scan endpoint."""
    if request.method == 'OPTIONS':
        return '', 204
    
    print(f"📡 Start scan requested: {request.get_json()}")
    event = {
        'httpMethod': 'POST',
        'path': '/scan/start',
        'body': json.dumps(request.get_json()),
        'requestContext': {
            'authorizer': {
                'user_id': 'local-test-user'
            }
        }
    }
    return lambda_to_flask(start_scan_handler, event)


@app.route('/scan/<scan_id>/status', methods=['GET'])
def get_status(scan_id):
    """Get scan status endpoint."""
    print(f"📡 Get status requested: {scan_id}")
    event = {
        'httpMethod': 'GET',
        'path': f'/scan/{scan_id}/status',
        'pathParameters': {
            'scan_id': scan_id
        },
        'requestContext': {
            'authorizer': {
                'user_id': 'local-test-user'
            }
        }
    }
    return lambda_to_flask(get_status_handler, event)


@app.route('/scan/<scan_id>/result', methods=['GET'])
def get_result(scan_id):
    """Get scan result endpoint."""
    print(f"📡 Get result requested: {scan_id}")
    event = {
        'httpMethod': 'GET',
        'path': f'/scan/{scan_id}/result',
        'pathParameters': {
            'scan_id': scan_id
        },
        'requestContext': {
            'authorizer': {
                'user_id': 'local-test-user'
            }
        }
    }
    return lambda_to_flask(get_result_handler, event)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Zentrion Backend Local Server")
    print("=" * 60)
    print("Server running on: http://localhost:5000")
    print("\n📍 Available endpoints:")
    print("  GET  http://localhost:5000/health")
    print("  POST http://localhost:5000/scan/start")
    print("  GET  http://localhost:5000/scan/{scan_id}/status")
    print("  GET  http://localhost:5000/scan/{scan_id}/result")
    print("\n💡 Tips:")
    print("  - Frontend should connect to: http://localhost:5000")
    print("  - Use run_scan.py to process scans manually")
    print("  - Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)