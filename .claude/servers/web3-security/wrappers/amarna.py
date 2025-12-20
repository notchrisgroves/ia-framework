#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
amarna wrapper - MCP Code API Pattern (VPS Docker deployment)
Executes amarna linter, saves raw output, returns parsed summary

Token Optimization: 92.8% reduction (saves full SARIF output, returns summary)
Note: Older tool, primarily for basic linting and code quality
"""

import sys
import io
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def amarna_lint(contract_path: str, rules: str = "", engagement_dir: Optional[str] = None) -> Dict:
    """
    Execute Amarna static analysis and linting on Cairo contracts.

    Args:
        contract_path: Path to Cairo file or project directory
        rules: Optional comma-separated rule names
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with:
        - summary: Parsed findings (by severity, rule type)
        - outputFile: Path to raw SARIF output
        - message: Human-readable summary
    """

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_name = re.sub(r'[^\w\-]', '_', contract_path.split('/')[-1])
    filename = f"{safe_name}-{timestamp}.sarif"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "amarna"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "amarna"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command (Amarna outputs SARIF format)
    cmd = f"amarna {contract_path} -o {output_file}"
    if rules:
        cmd += f" --rules {rules}"

    try:
        result = docker_exec("web3-security", cmd, timeout=180)

        # Amarna may return non-zero with findings
        if not output_file.exists():
            # Save stdout/stderr as fallback
            text_file = output_dir / filename.replace('.sarif', '.txt')
            text_file.write_text(result["stdout"] + result["stderr"], encoding='utf-8')

            return {
                "error": f"Amarna execution failed: {result["stderr"]}",
                "outputFile": str(text_file)
            }

        # Parse the SARIF output
        summary = parse_amarna_output(output_file)

        # Generate message
        total = summary["totalIssues"]
        message = f"[+] Amarna linting complete\n"
        message += f"    Target: {contract_path}\n"
        message += f"    Issues found: {total}\n"

        if summary["bySeverity"]:
            message += f"    By severity:\n"
            for sev in ['error', 'warning', 'note']:
                if sev in summary["bySeverity"]:
                    message += f"      {sev}: {summary['bySeverity'][sev]}\n"

        if summary["topIssues"]:
            message += f"    Top issues (first 5):\n"
            for issue in summary["topIssues"][:5]:
                message += f"      [{issue['level']}] {issue['ruleId']}: {issue['message'][:80]}...\n"

        message += f"    Full results: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Amarna timed out (3 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"Amarna execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def parse_amarna_output(filepath: Path) -> Dict:
    """Parse Amarna SARIF output file."""

    if not filepath.exists():
        return {
            "totalIssues": 0,
            "bySeverity": {},
            "byRule": {},
            "topIssues": []
        }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {
            "totalIssues": 0,
            "bySeverity": {},
            "byRule": {},
            "topIssues": []
        }

    # SARIF structure: runs[0].results[]
    runs = data.get('runs', [])
    if not runs:
        return {
            "totalIssues": 0,
            "bySeverity": {},
            "byRule": {},
            "topIssues": []
        }

    results = runs[0].get('results', [])

    by_severity = {}
    by_rule = {}
    top_issues = []

    for result in results:
        level = result.get('level', 'note')  # error, warning, note
        rule_id = result.get('ruleId', 'unknown')
        message = result.get('message', {}).get('text', '')

        # Count by severity
        by_severity[level] = by_severity.get(level, 0) + 1

        # Count by rule
        by_rule[rule_id] = by_rule.get(rule_id, 0) + 1

        # Collect top issues
        location = result.get('locations', [{}])[0]
        physical_location = location.get('physicalLocation', {})
        artifact = physical_location.get('artifactLocation', {}).get('uri', '')
        region = physical_location.get('region', {})
        line = region.get('startLine', 0)

        top_issues.append({
            "level": level,
            "ruleId": rule_id,
            "message": message,
            "file": artifact,
            "line": line
        })

    return {
        "totalIssues": len(results),
        "bySeverity": by_severity,
        "byRule": by_rule,
        "topIssues": top_issues[:20]  # Top 20
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python amarna.py <contract_path> [rules] [engagement_dir]")
        print("")
        print("Examples:")
        print("  python amarna.py contract.cairo")
        print("  python amarna.py project/ 'unused-imports,unsafe-math'")
        print("")
        print("Note: Older tool, primarily for basic linting and code quality checks")
        sys.exit(1)

    contract_path = sys.argv[1]
    rules = sys.argv[2] if len(sys.argv) > 2 else ""
    engagement_dir = sys.argv[3] if len(sys.argv) > 3 else None

    result = amarna_lint(contract_path, rules, engagement_dir)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
