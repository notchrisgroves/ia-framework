#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mythril wrapper - MCP Code API Pattern (VPS Docker deployment)
Executes mythril, saves raw output, returns parsed summary
"""

import sys
import io
import json
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


def mythril(contract_path: str = "", contract_address: str = "", rpc_url: str = "", engagement_dir: Optional[str] = None) -> Dict:
    """
    Execute mythril security analysis using symbolic execution.

    Args:
        contract_path: Path to Solidity file (for source analysis)
        contract_address: Contract address (for deployed contract analysis)
        rpc_url: RPC URL (required for deployed contract analysis)
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with:
        - summary: Parsed findings (security issues by severity)
        - outputFile: Path to raw mythril output (JSON format)
        - message: Human-readable summary
    """

    if not contract_path and not contract_address:
        return {
            "error": "Either contract_path or contract_address is required",
            "outputFile": ""
        }

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    target_name = contract_address if contract_address else Path(contract_path).stem
    filename = f"{target_name}-{timestamp}.json"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "mythril"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "mythril"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command
    if contract_address:
        if not rpc_url:
            return {"error": "rpc_url required for deployed contract analysis", "outputFile": str(output_file)}
        cmd = f"myth analyze -a {contract_address} --rpc {rpc_url} -o json"
    else:
        cmd = f"myth analyze {contract_path} -o json"

    cmd += f" > {output_file} 2>&1"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            timeout=600  # 10 minute timeout
        )

        if not output_file.exists():
            return {
                "error": "mythril execution failed - no output file created",
                "outputFile": str(output_file)
            }

        # Parse the output
        summary = parse_mythril_output(output_file)

        # Generate message
        message = f"[+] mythril analysis complete\n"
        message += f"    Target: {contract_address or contract_path}\n"
        message += f"    Issues found: {summary['totalIssues']}\n"

        if summary["bySeverity"]:
            message += f"    By severity:\n"
            for sev in ['High', 'Medium', 'Low']:
                if sev in summary["bySeverity"]:
                    message += f"      {sev}: {summary['bySeverity'][sev]}\n"

        if summary["topIssues"]:
            message += f"    Top issues (first 5):\n"
            for issue in summary["topIssues"][:5]:
                message += f"      [{issue['severity']}] {issue['title']}\n"

        message += f"    Full results: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "mythril timed out (10 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"mythril execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def parse_mythril_output(filepath: Path) -> Dict:
    """Parse mythril JSON output file."""

    if not filepath.exists():
        return {
            "totalIssues": 0,
            "bySeverity": {},
            "topIssues": []
        }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Mythril output may have text before JSON
            content = f.read()
            # Find JSON portion
            json_start = content.find('{')
            if json_start == -1:
                return {"totalIssues": 0, "bySeverity": {}, "topIssues": []}
            data = json.loads(content[json_start:])
    except (json.JSONDecodeError, ValueError):
        return {"totalIssues": 0, "bySeverity": {}, "topIssues": []}

    issues = data.get('issues', [])
    by_severity = {}
    top_issues = []

    for issue in issues:
        severity = issue.get('severity', 'Unknown')
        by_severity[severity] = by_severity.get(severity, 0) + 1

        top_issues.append({
            "title": issue.get('title', 'Unknown'),
            "severity": severity,
            "swc_id": issue.get('swc-id', ''),
            "description": issue.get('description', '')[:200]
        })

    return {
        "totalIssues": len(issues),
        "bySeverity": by_severity,
        "topIssues": top_issues
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mythril.py <contract_path or address> [rpc_url] [engagement_dir]")
        print("Example: python mythril.py Token.sol")
        print("Example: python mythril.py 0xABCD... https://eth.llamarpc.com")
        sys.exit(1)

    arg1 = sys.argv[1]
    # Detect if arg is address (0x...) or file path
    if arg1.startswith('0x'):
        contract_address = arg1
        contract_path = ""
        rpc_url = sys.argv[2] if len(sys.argv) > 2 else ""
        engagement_dir = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        contract_path = arg1
        contract_address = ""
        rpc_url = ""
        engagement_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = mythril(contract_path, contract_address, rpc_url, engagement_dir)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
