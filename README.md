# semgrep-lite

Custom static analysis rules in simple YAML. Cross-language.

## Install

```bash
git clone https://github.com/openkickstartai/semgrep-lite.git
cd semgrep-lite && pip install -e .
```

## Usage

```bash
# Run rules against your code
semgrep-lite scan --rules rules/ src/

# Check a single rule
semgrep-lite scan --rules no-eval.yml .

# List built-in rules
semgrep-lite list-rules
```

## Writing rules

```yaml
id: no-eval
language: python
severity: error
message: "Do not use eval() - it executes arbitrary code"
pattern: "eval("
```

```yaml
id: no-console-log
language: javascript
severity: warning
message: "Remove console.log before committing"
pattern: "console.log("
```

## Testing

```bash
pytest -v
```
