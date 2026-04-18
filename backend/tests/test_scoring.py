"""
Tests for core_scoring module.
Severity weights: CRITICAL=-25, HIGH=-15, MEDIUM=-7, LOW=-3, INFO=0
Grade thresholds: A>=90, B>=80, C>=70, D>=60, F>=0
"""
import pytest
from src.core.core_scoring import calculate_hygiene_score, ScoringEngine
from src.models.models_scan_result import ToolResult
from src.config.config_constants import ScanCategory


def _make_result(tool, category, critical=0, high=0, medium=0, low=0, info=0):
    return ToolResult(
        tool=tool,
        category=category,
        severity={"critical": critical, "high": high, "medium": medium, "low": low, "info": info},
        issues=[],
        execution_time=0.1,
        status="success"
    )


class TestScoringEngine:
    def test_no_issues_returns_perfect_score(self):
        score = calculate_hygiene_score([_make_result("headers", ScanCategory.HEADERS)])
        assert score.score == 100
        assert score.grade == "A"
        assert score.total_issues == 0

    def test_empty_results_returns_perfect_score(self):
        score = calculate_hygiene_score([])
        assert score.score == 100

    def test_one_critical_reduces_by_25(self):
        # 100 + (-25) = 75
        score = calculate_hygiene_score([_make_result("h", ScanCategory.HEADERS, critical=1)])
        assert score.score == 75
        assert score.critical_count == 1

    def test_three_high_reduces_to_55(self):
        # 100 + (3 * -15) = 55
        score = calculate_hygiene_score([_make_result("t", ScanCategory.TLS, high=3)])
        assert score.score == 55
        assert score.grade == "F"
        assert score.high_count == 3

    def test_score_clamps_to_zero(self):
        # 100 + (10 * -25) = -150 → clamped to 0
        score = calculate_hygiene_score([_make_result("h", ScanCategory.HEADERS, critical=10)])
        assert score.score == 0
        assert score.grade == "F"

    def test_info_issues_do_not_affect_score(self):
        score = calculate_hygiene_score([_make_result("h", ScanCategory.HEADERS, info=5)])
        assert score.score == 100
        assert score.total_issues == 5

    def test_mixed_tools_aggregate_correctly(self):
        # headers: 1H + 2M → -15 + -14 = -29
        # tls:     1M + 1L → -7  + -3  = -10
        # total: 100 - 29 - 10 = 61, total_issues = 5
        results = [
            _make_result("headers", ScanCategory.HEADERS, high=1, medium=2),
            _make_result("tls", ScanCategory.TLS, medium=1, low=1),
        ]
        score = calculate_hygiene_score(results)
        assert score.score == 61
        assert score.grade == "D"
        assert score.total_issues == 5
        assert score.high_count == 1
        assert score.medium_count == 3
        assert score.low_count == 1

    def test_grade_boundaries(self):
        engine = ScoringEngine()
        assert engine._get_grade(90)[0] == "A"
        assert engine._get_grade(89)[0] == "B"
        assert engine._get_grade(80)[0] == "B"
        assert engine._get_grade(79)[0] == "C"
        assert engine._get_grade(70)[0] == "C"
        assert engine._get_grade(69)[0] == "D"
        assert engine._get_grade(60)[0] == "D"
        assert engine._get_grade(59)[0] == "F"
        assert engine._get_grade(0)[0] == "F"
