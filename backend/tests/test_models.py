"""
Tests for Pydantic model validation.
"""
import pytest
from pydantic import ValidationError
from src.models.models_scan_request import ScanRequest
from src.models.models_scan_result import ToolResult, SecurityScore
from src.config.config_constants import ScanType, ScanCategory


class TestScanRequest:
    def test_valid_quick_scan(self):
        req = ScanRequest(target="https://example.com", scan_type="quick")
        assert req.target == "https://example.com"
        assert req.scan_type == ScanType.QUICK

    def test_default_scan_type_is_quick(self):
        req = ScanRequest(target="https://example.com")
        assert req.scan_type == ScanType.QUICK

    def test_full_scan_type(self):
        req = ScanRequest(target="https://example.com", scan_type="full")
        assert req.scan_type == ScanType.FULL

    def test_url_without_scheme_gets_https(self):
        req = ScanRequest(target="example.com")
        assert req.target == "https://example.com"

    def test_missing_target_raises_error(self):
        with pytest.raises(ValidationError):
            ScanRequest()

    def test_invalid_scan_type_raises_error(self):
        with pytest.raises(ValidationError):
            ScanRequest(target="https://example.com", scan_type="extreme")

    def test_optional_github_repo(self):
        req = ScanRequest(
            target="https://example.com",
            github_repo="https://github.com/user/repo"
        )
        assert req.github_repo == "https://github.com/user/repo"

    def test_optional_github_repo_defaults_none(self):
        req = ScanRequest(target="https://example.com")
        assert req.github_repo is None


class TestToolResult:
    def test_valid_tool_result(self):
        result = ToolResult(
            tool="headers",
            category=ScanCategory.HEADERS,
            severity={"critical": 0, "high": 1, "medium": 0, "low": 0, "info": 0},
            issues=[],
            execution_time=0.5,
            status="success"
        )
        assert result.tool == "headers"
        assert result.severity["high"] == 1

    def test_default_severity_all_zero(self):
        result = ToolResult(
            tool="tls",
            category=ScanCategory.TLS,
            execution_time=1.0
        )
        for severity in ["critical", "high", "medium", "low", "info"]:
            assert result.severity[severity] == 0

    def test_default_status_is_success(self):
        result = ToolResult(tool="headers", category=ScanCategory.HEADERS, execution_time=0.1)
        assert result.status == "success"


class TestSecurityScore:
    def test_valid_score(self):
        score = SecurityScore(
            score=85,
            grade="B",
            summary="Good security with minor issues",
            total_issues=2,
            high_count=1
        )
        assert score.score == 85
        assert score.grade == "B"

    def test_score_100_valid(self):
        score = SecurityScore(score=100, grade="A", summary="Perfect")
        assert score.score == 100

    def test_score_0_valid(self):
        score = SecurityScore(score=0, grade="F", summary="Critical issues")
        assert score.score == 0

    def test_score_above_100_raises(self):
        with pytest.raises(ValidationError):
            SecurityScore(score=101, grade="A", summary="test")

    def test_score_negative_raises(self):
        with pytest.raises(ValidationError):
            SecurityScore(score=-1, grade="F", summary="test")
