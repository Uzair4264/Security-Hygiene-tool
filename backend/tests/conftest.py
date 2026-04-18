"""
Shared pytest fixtures. Env vars must be set before any src imports
because Settings reads them at class-definition time.
"""
import os
import pytest

os.environ.setdefault("LOCAL_MODE", "true")
os.environ.setdefault("ALLOW_ANONYMOUS", "true")
os.environ.setdefault("JWT_SECRET", "test-secret-key-not-for-production")
os.environ.setdefault("DYNAMODB_TABLE", "test-scans-table")
os.environ.setdefault("STAGE", "test")


@pytest.fixture
def sample_valid_url():
    return "https://example.com"


@pytest.fixture
def sample_invalid_url():
    return "not-a-url"


@pytest.fixture
def sample_private_url():
    return "http://192.168.1.1"


@pytest.fixture
def sample_localhost_url():
    return "http://localhost:8080"


@pytest.fixture
def mock_lambda_event():
    return {
        "httpMethod": "POST",
        "path": "/scan/start",
        "body": '{"target": "https://example.com", "scan_type": "quick"}',
        "requestContext": {
            "authorizer": {
                "user_id": "test-user-fixture"
            }
        }
    }


@pytest.fixture
def mock_lambda_context():
    class MockContext:
        function_name = "test-function"
        function_version = "$LATEST"
        invoked_function_arn = "arn:aws:lambda:us-east-1:123456789:function:test"
        memory_limit_in_mb = 128
        aws_request_id = "test-request-id"
        log_group_name = "/aws/lambda/test"
        log_stream_name = "test-stream"

        def get_remaining_time_in_millis(self):
            return 30000

    return MockContext()
