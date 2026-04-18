"""
Tests for utils_validators module.
"""
import pytest
from src.utils.utils_validators import (
    validate_url,
    validate_github_repo,
    validate_scan_type,
    validate_environment,
)


class TestValidateUrl:
    def test_valid_https_url(self, sample_valid_url):
        is_valid, msg = validate_url(sample_valid_url)
        assert is_valid is True
        assert msg is None

    def test_valid_http_url(self):
        is_valid, msg = validate_url("http://example.com")
        assert is_valid is True

    def test_empty_string(self):
        is_valid, msg = validate_url("")
        assert is_valid is False
        assert msg == "URL is required"

    def test_none_url(self):
        is_valid, msg = validate_url(None)
        assert is_valid is False

    def test_invalid_format(self, sample_invalid_url):
        is_valid, msg = validate_url(sample_invalid_url)
        assert is_valid is False
        assert "Invalid URL format" in msg

    def test_localhost_blocked(self, sample_localhost_url):
        # validators.url() rejects "localhost" as an invalid domain before our check
        is_valid, msg = validate_url(sample_localhost_url)
        assert is_valid is False

    def test_127_blocked(self):
        is_valid, msg = validate_url("http://127.0.0.1/admin")
        assert is_valid is False

    def test_private_ip_192_blocked(self, sample_private_url):
        is_valid, msg = validate_url(sample_private_url)
        assert is_valid is False
        assert "private" in msg.lower()

    def test_private_ip_10_blocked(self):
        is_valid, msg = validate_url("http://10.0.0.1/internal")
        assert is_valid is False

    def test_ftp_scheme_blocked(self):
        is_valid, msg = validate_url("ftp://example.com/file")
        assert is_valid is False
        assert "HTTP or HTTPS" in msg


class TestValidateGithubRepo:
    def test_valid_github_url(self):
        is_valid, msg = validate_github_repo("https://github.com/user/repo")
        assert is_valid is True
        assert msg is None

    def test_none_is_valid(self):
        is_valid, msg = validate_github_repo(None)
        assert is_valid is True

    def test_empty_string_is_valid(self):
        is_valid, msg = validate_github_repo("")
        assert is_valid is True

    def test_non_github_blocked(self):
        is_valid, msg = validate_github_repo("https://gitlab.com/user/repo")
        assert is_valid is False
        assert "GitHub" in msg

    def test_invalid_url_format(self):
        is_valid, msg = validate_github_repo("not-a-url")
        assert is_valid is False


class TestValidateScanType:
    def test_quick_valid(self):
        is_valid, msg = validate_scan_type("quick")
        assert is_valid is True

    def test_full_valid(self):
        is_valid, msg = validate_scan_type("full")
        assert is_valid is True

    def test_invalid_type(self):
        is_valid, msg = validate_scan_type("deep")
        assert is_valid is False

    def test_case_insensitive(self):
        is_valid, msg = validate_scan_type("QUICK")
        assert is_valid is True

    def test_empty_string(self):
        is_valid, msg = validate_scan_type("")
        assert is_valid is False


class TestValidateEnvironment:
    def test_none_is_valid(self):
        is_valid, msg = validate_environment(None)
        assert is_valid is True

    def test_dev_valid(self):
        is_valid, msg = validate_environment("dev")
        assert is_valid is True

    def test_staging_valid(self):
        is_valid, msg = validate_environment("staging")
        assert is_valid is True

    def test_production_valid(self):
        is_valid, msg = validate_environment("production")
        assert is_valid is True

    def test_invalid_environment(self):
        is_valid, msg = validate_environment("qa")
        assert is_valid is False
