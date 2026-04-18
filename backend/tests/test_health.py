"""
Tests for the health check Lambda handler.
"""
import json
import pytest
from src.api.api_health import handler


class TestHealthHandler:
    def test_returns_200(self, mock_lambda_context):
        response = handler({}, mock_lambda_context)
        assert response["statusCode"] == 200

    def test_body_is_valid_json(self, mock_lambda_context):
        response = handler({}, mock_lambda_context)
        body = json.loads(response["body"])
        assert isinstance(body, dict)

    def test_success_true(self, mock_lambda_context):
        response = handler({}, mock_lambda_context)
        body = json.loads(response["body"])
        assert body["success"] is True

    def test_returns_healthy_status(self, mock_lambda_context):
        response = handler({}, mock_lambda_context)
        body = json.loads(response["body"])
        assert body["data"]["status"] == "healthy"

    def test_returns_service_name(self, mock_lambda_context):
        response = handler({}, mock_lambda_context)
        body = json.loads(response["body"])
        assert body["data"]["service"] == "zentrion-backend"

    def test_cors_header_present(self, mock_lambda_context):
        response = handler({}, mock_lambda_context)
        assert "Access-Control-Allow-Origin" in response["headers"]
