"""
Security hygiene scoring engine.
"""
from typing import List, Dict, Any

from src.models.models_scan_result import ToolResult, SecurityScore
from src.config.config_constants import SEVERITY_WEIGHTS, SCORE_GRADES, Severity
from src.utils.utils_logger import get_logger
from src.utils.value_normalizer import normalize_value


logger = get_logger(__name__)


class ScoringEngine:
    """Calculate security hygiene scores from scan results."""
    
    BASE_SCORE = 100
    MIN_SCORE = 0
    MAX_SCORE = 100
    
    @staticmethod
    def calculate_score(tool_results: List[ToolResult]) -> SecurityScore:
        """
        Calculate security hygiene score from tool results.

        Args:
            tool_results: Results from security scanning tools

        Returns:
            Security score with breakdown
        """
        logger.info("Calculating security score", num_tools=len(tool_results))

        # Start with base score
        score = ScoringEngine.BASE_SCORE

        # Count issues by severity
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }

        category_impact = {}

        # Process each tool result
        for result in tool_results:
            # Add to severity counts
            for severity, count in result.severity.items():
                severity_counts[severity] += count

            # Calculate impact for this category
            category_score = 0
            for severity, count in result.severity.items():
                # Handle both string and enum severities
                sev_enum = Severity(severity) if isinstance(severity, str) else severity
                category_score += SEVERITY_WEIGHTS[sev_enum] * count

            # Handle category name safely
            category_name = result.category.value if hasattr(result.category, "value") else str(result.category)
            category_impact[category_name] = category_score

            # Apply to total score
            score += category_score

        # Clamp score to valid range
        score = max(ScoringEngine.MIN_SCORE, min(score, ScoringEngine.MAX_SCORE))

        # Determine grade
        grade, summary = ScoringEngine._get_grade(score)

        # Calculate total issues
        total_issues = sum(severity_counts.values())

        logger.info(
            "Score calculated",
            score=score,
            grade=grade,
            total_issues=total_issues,
            critical=severity_counts["critical"],
            high=severity_counts["high"]
        )

        return SecurityScore(
            score=int(score),
            grade=grade,
            summary=summary,
            total_issues=total_issues,
            critical_count=severity_counts["critical"],
            high_count=severity_counts["high"],
            medium_count=severity_counts["medium"],
            low_count=severity_counts["low"],
            breakdown=category_impact
        )

    
    @staticmethod
    def _get_grade(score: int) -> tuple[str, str]:
        """
        Get letter grade and summary for score.
        
        Args:
            score: Numeric score (0-100)
            
        Returns:
            Tuple of (grade, summary)
        """
        for threshold, grade, summary in SCORE_GRADES:
            if score >= threshold:
                return grade, summary
        
        return "F", "Critical security vulnerabilities"


def calculate_hygiene_score(tool_results: List[ToolResult]) -> SecurityScore:
    """
    Convenience function to calculate hygiene score.
    
    Args:
        tool_results: Results from security tools
        
    Returns:
        Security score
    """
    engine = ScoringEngine()
    return engine.calculate_score(tool_results)