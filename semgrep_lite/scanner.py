"""Core scanner."""
import os
from typing import List, Dict

LANG_EXTENSIONS = {
    'python': ['.py'],
    'javascript': ['.js', '.jsx', '.ts', '.tsx'],
    'go': ['.go'],
    'ruby': ['.rb'],
}

class Scanner:
    def __init__(self, rules: List[Dict]):
        self.rules = rules

    def scan_path(self, path: str) -> List[Dict]:
        findings = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__', 'venv')]
            for fname in files:
                fpath = os.path.join(root, fname)
                ext = os.path.splitext(fname)[1]
                for rule in self.rules:
                    lang = rule.get('language', '')
                    if lang and ext not in LANG_EXTENSIONS.get(lang, [ext]):
                        continue
                    findings.extend(self._scan_file(fpath, rule))
        return findings

    def _scan_file(self, path: str, rule: Dict) -> List[Dict]:
        findings = []
        pattern = rule.get('pattern', '')
        if not pattern:
            return findings
        try:
            with open(path, 'r', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if pattern in line:
                        findings.append({
                            'rule': rule.get('id', 'unknown'),
                            'file': path,
                            'line': i,
                            'severity': rule.get('severity', 'warning'),
                            'message': rule.get('message', f'Pattern matched: {pattern}'),
                            'match': line.rstrip()[:120],
                        })
        except (OSError, UnicodeDecodeError):
            pass
        return findings
