"""CLI entry point."""
import click
import os
import time
from semgrep_lite.scanner import Scanner
from semgrep_lite.rules import load_rules

@click.group()
def main():
    """Simple code rules in YAML."""
    pass

@main.command()
@click.option('--rules', '-r', required=True, help='Rules file or directory')
@click.option('--timing', is_flag=True, help='Show timing information')
@click.argument('path', default='.')
def scan(rules, timing, path):
    """Scan code against rules."""
    start_time = time.perf_counter()
    
    rule_list = load_rules(rules)
    scanner = Scanner(rule_list)
    findings = scanner.scan_path(path)
    
    scan_time = time.perf_counter() - start_time
    
    # Batch output for better performance
    output_lines = []
    for f in findings:
        sev = f['severity'].upper()
        output_lines.append(f"  [{sev}] {f['file']}:{f['line']} - {f['message']}")
    
    if output_lines:
        click.echo('\n'.join(output_lines))
        click.echo(f"\n{len(findings)} finding(s)")
        if timing:
            click.echo(f"Scan completed in {scan_time:.3f}s")
        raise SystemExit(1)
    else:
        click.echo("No findings. All clear.")
        if timing:
            click.echo(f"Scan completed in {scan_time:.3f}s")
