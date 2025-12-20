#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slither wrapper - MCP Code API Pattern (VPS Docker deployment)
Executes slither, saves raw output, returns parsed summary
"""

import sys
import io
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def slither(contract_path: str, detectors: str = "", engagement_dir: Optional[str] = None) -> Dict:
    """
    Execute slither static analysis on Solidity contracts.

    Args:
        contract_path: Path to Solidity file or GitHub repo URL
        detectors: Optional comma-separated detector names
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with:
        - summary: Parsed findings (by severity, detector type)
        - outputFile: Path to raw slither output (JSON format)
        - message: Human-readable summary
    """

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_name = re.sub(r'[^\w\-]', '_', contract_path.split('/')[-1])
    filename = f"{safe_name}-{timestamp}.json"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "slither"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "slither"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command (JSON output for better parsing)
    cmd = f"slither {contract_path} --json {output_file}"
    if detectors:
        cmd += f" --detect {detectors}"

    try:
        result = docker_exec("web3-security", cmd, timeout=300)

        # Slither may return non-zero with findings
        if not output_file.exists():
            return {
                "error": f"slither execution failed: {result["stderr"]}",
                "outputFile": str(output_file)
            }

        # Parse the output
        summary = parse_slither_output(output_file)

        # Generate message
        total = summary["totalIssues"]
        message = f"[+] slither analysis complete\n"
        message += f"    Target: {contract_path}\n"
        message += f"    Issues found: {total}\n"

        if summary["bySeverity"]:
            message += f"    By severity:\n"
            for sev in ['High', 'Medium', 'Low', 'Informational']:
                if sev in summary["bySeverity"]:
                    message += f"      {sev}: {summary['bySeverity'][sev]}\n"

        if summary["topIssues"]:
            message += f"    Top issues (first 5):\n"
            for issue in summary["topIssues"][:5]:
                message += f"      [{issue['severity']}] {issue['check']}: {issue['description'][:80]}...\n"

        message += f"    Full results: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "slither timed out (5 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"slither execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def parse_slither_output(filepath: Path) -> Dict:
    """Parse slither JSON output file."""

    if not filepath.exists():
        return {
            "totalIssues": 0,
            "bySeverity": {},
            "byDetector": {},
            "topIssues": []
        }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {
            "totalIssues": 0,
            "bySeverity": {},
            "byDetector": {},
            "topIssues": []
        }

    results = data.get('results', {})
    detectors = results.get('detectors', [])

    by_severity = {}
    by_detector = {}
    top_issues = []

    for issue in detectors:
        severity = issue.get('impact', 'Unknown')
        check = issue.get('check', 'unknown')
        description = issue.get('description', '')

        # Count by severity
        by_severity[severity] = by_severity.get(severity, 0) + 1

        # Count by detector
        by_detector[check] = by_detector.get(check, 0) + 1

        # Collect top issues
        top_issues.append({
            "severity": severity,
            "check": check,
            "description": description,
            "confidence": issue.get('confidence', ''),
            "elements": len(issue.get('elements', []))
        })

    return {
        "totalIssues": len(detectors),
        "bySeverity": by_severity,
        "byDetector": by_detector,
        "topIssues": top_issues[:20]  # Top 20
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python slither.py <contract_path> [detectors] [engagement_dir]")
        print("Example: python slither.py Token.sol")
        print("Example: python slither.py https://github.com/user/repo 'reentrancy-eth,access-control'")
        sys.exit(1)

    contract_path = sys.argv[1]
    detectors = sys.argv[2] if len(sys.argv) > 2 else ""
    engagement_dir = sys.argv[3] if len(sys.argv) > 3 else None

    result = slither(contract_path, detectors, engagement_dir)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
