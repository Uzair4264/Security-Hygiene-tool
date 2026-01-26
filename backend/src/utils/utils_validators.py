"""
Validation utilities for inputs.
"""
import re
from typing import Optional
from urllib.parse import urlparse

import validators


def validate_url(url: str) -> tuple[bool, Optional[str]]:
    """
    Validate URL format and security.
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "URL is required"
    
    # Check basic format
    if not validators.url(url):
        return False, "Invalid URL format"
    
    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        return False, f"Failed to parse URL: {str(e)}"
    
    # Check scheme
    if parsed.scheme not in ["http", "https"]:
        return False, "URL must use HTTP or HTTPS protocol"
    
    # Check for localhost/internal IPs in production
    if parsed.hostname:
        if parsed.hostname in ["localhost", "127.0.0.1", "0.0.0.0"]:
            return False, "Cannot scan localhost or loopback addresses"
        
        # Check for private IP ranges
        if _is_private_ip(parsed.hostname):
            return False, "Cannot scan private IP addresses"
    
    return True, None


def _is_private_ip(hostname: str) -> bool:
    """Check if hostname is a private IP address."""
    private_patterns = [
        r'^10\.',
        r'^172\.(1[6-9]|2[0-9]|3[0-1])\.',
        r'^192\.168\.',
        r'^169\.254\.',
    ]
    
    for pattern in private_patterns:
        if re.match(pattern, hostname):
            return True
    
    return False


def validate_scan_type(scan_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate scan type.
    
    Args:
        scan_type: Type of scan to perform
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_types = ["quick", "full"]
    
    if not scan_type:
        return False, "Scan type is required"
    
    if scan_type.lower() not in valid_types:
        return False, f"Scan type must be one of: {', '.join(valid_types)}"
    
    return True, None


def validate_environment(environment: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate environment type.
    
    Args:
        environment: Target environment
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not environment:
        return True, None  # Optional field
    
    valid_envs = ["dev", "staging", "production"]
    
    if environment.lower() not in valid_envs:
        return False, f"Environment must be one of: {', '.join(valid_envs)}"
    
    return True, None


def validate_github_repo(repo_url: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate GitHub repository URL.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not repo_url:
        return True, None  # Optional field
    
    if not validators.url(repo_url):
        return False, "Invalid repository URL format"
    
    # Check if it's a GitHub URL
    parsed = urlparse(repo_url)
    if parsed.hostname not in ["github.com", "www.github.com"]:
        return False, "Repository must be hosted on GitHub"
    
    return True, None