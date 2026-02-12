"""semgrep-lite: Simple YAML-based code rules."""
import re

__version__ = "0.1.0"

def sanitize_path(path):
    """Sanitize file paths to prevent directory traversal."""
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    # Remove null bytes and normalize path
    clean_path = path.replace('\0', '').strip()
    # Prevent directory traversal
    if '..' in clean_path or clean_path.startswith('/'):
        raise ValueError("Invalid path detected")
    return clean_path

def validate_yaml_content(content):
    """Basic validation for YAML content."""
    if not isinstance(content, str):
        raise ValueError("Content must be a string")
    # Check for potentially dangerous patterns
    dangerous_patterns = [r'!!python/', r'__import__', r'eval\(', r'exec\(']
    for pattern in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            raise ValueError(f"Potentially dangerous content detected: {pattern}")
    return content
