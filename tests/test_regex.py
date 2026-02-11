"""Tests for regex scanning."""
from semgrep_lite.regex_scanner import scan_with_regex

def test_regex_match():
    rule = {'id': 'todo', 'pattern': r'TODO\s*:', 'regex': True, 'severity': 'warning', 'message': 'Found TODO'}
    findings = scan_with_regex('# TODO: fix this\nprint(1)\n', rule)
    assert len(findings) == 1
    assert findings[0]['line'] == 1

def test_regex_no_match():
    rule = {'id': 'todo', 'pattern': r'TODO\s*:', 'regex': True, 'severity': 'warning', 'message': 'Found TODO'}
    findings = scan_with_regex('print("hello")\n', rule)
    assert len(findings) == 0

def test_substring_mode():
    rule = {'id': 'eval', 'pattern': 'eval(', 'severity': 'error', 'message': 'no eval'}
    findings = scan_with_regex('x = eval(input())\n', rule)
    assert len(findings) == 1

def test_capture_group_in_message():
    rule = {'id': 'ip', 'pattern': r'(\d+\.\d+\.\d+\.\d+)', 'regex': True, 'severity': 'warning',
            'message': 'Hardcoded IP: {match}'}
    findings = scan_with_regex('host = "192.168.1.1"\n', rule)
    assert '192.168.1.1' in findings[0]['message']
