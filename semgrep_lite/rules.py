"""Rule loading."""
import os
import yaml
from typing import List, Dict

def load_rules(path: str) -> List[Dict]:
    """Load rules from a YAML file or directory."""
    rules = []
    if os.path.isfile(path):
        rules.extend(_load_file(path))
    elif os.path.isdir(path):
        for f in sorted(os.listdir(path)):
            if f.endswith(('.yml', '.yaml')):
                rules.extend(_load_file(os.path.join(path, f)))
    return rules

def _load_file(path: str) -> List[Dict]:
    with open(path) as f:
        data = yaml.safe_load(f)
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    return []
