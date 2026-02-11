"""CLI entry point."""
import click
import os
from semgrep_lite.scanner import Scanner
from semgrep_lite.rules import load_rules

@click.group()
def main():
    """Simple code rules in YAML."""
    pass

@main.command()
@click.option('--rules', '-r', required=True, help='Rules file or directory')
@click.argument('path', default='.')
def scan(rules, path):
    """Scan code against rules."""
    rule_list = load_rules(rules)
    scanner = Scanner(rule_list)
    findings = scanner.scan_path(path)
    for f in findings:
        sev = f['severity'].upper()
        click.echo(f"  [{sev}] {f['file']}:{f['line']} - {f['message']}")
    if findings:
        click.echo(f"\n{len(findings)} finding(s)")
        raise SystemExit(1)
    else:
        click.echo("No findings. All clear.")
