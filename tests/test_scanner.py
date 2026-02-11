"""Tests for scanner."""
import os
import tempfile
from semgrep_lite.scanner import Scanner
from semgrep_lite.rules import load_rules

def test_detect_eval():
    rules = [{'id': 'no-eval', 'language': 'python', 'pattern': 'eval(', 'severity': 'error', 'message': 'no eval'}]
    scanner = Scanner(rules)
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, 'bad.py')
        open(f, 'w').write('result = eval(user_input)\n')
        findings = scanner.scan_path(tmp)
        assert len(findings) == 1
        assert findings[0]['rule'] == 'no-eval'

def test_clean_code():
    rules = [{'id': 'no-eval', 'language': 'python', 'pattern': 'eval(', 'severity': 'error', 'message': 'no eval'}]
    scanner = Scanner(rules)
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, 'good.py')
        open(f, 'w').write('print("hello")\n')
        findings = scanner.scan_path(tmp)
        assert len(findings) == 0

def test_load_rules_file():
    with tempfile.NamedTemporaryFile(suffix='.yml', mode='w', delete=False) as f:
        f.write('id: test\npattern: TODO\nseverity: warning\nmessage: found todo\n')
        f.flush()
        rules = load_rules(f.name)
        assert len(rules) == 1
        assert rules[0]['id'] == 'test'
    os.unlink(f.name)

def test_respects_language():
    rules = [{'id': 'js-only', 'language': 'javascript', 'pattern': 'console.log', 'severity': 'warning', 'message': 'no log'}]
    scanner = Scanner(rules)
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, 'a.py'), 'w').write('console.log("test")\n')
        findings = scanner.scan_path(tmp)
        assert len(findings) == 0  # .py not matched for javascript rule
