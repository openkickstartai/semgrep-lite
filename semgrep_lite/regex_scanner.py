"""Regex-enhanced scanner."""
import re
from typing import Dict, List

def scan_with_regex(content: str, rule: Dict) -> List[Dict]:
    """Scan content with regex pattern."""
    pattern = rule.get('pattern', '')
    use_regex = rule.get('regex', False)
    findings = []
    for i, line in enumerate(content.split('\n'), 1):
        if use_regex:
            match = re.search(pattern, line)
            if match:
                findings.append({
                    'rule': rule.get('id', 'unknown'),
                    'line': i,
                    'severity': rule.get('severity', 'warning'),
                    'message': rule.get('message', '').replace('{match}', match.group(0)),
                    'match': line.rstrip()[:120],
                })
        else:
            if pattern in line:
                findings.append({
                    'rule': rule.get('id', 'unknown'),
                    'line': i,
                    'severity': rule.get('severity', 'warning'),
                    'message': rule.get('message', f'Pattern: {pattern}'),
                    'match': line.rstrip()[:120],
                })
    return findings
