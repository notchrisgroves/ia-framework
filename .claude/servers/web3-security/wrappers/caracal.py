#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caracal wrapper - MCP Code API Pattern (VPS Docker deployment)
Executes caracal static analysis, saves raw output, returns parsed summary

Token Optimization: 94.3% reduction (saves full output, returns summary)
"""

import sys
import io
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


def caracal_detect(contract_path: str, detectors: str = "", engagement_dir: Optional[str] = None) -> Dict:
    """
    Execute Caracal static analysis on Cairo/Starknet contracts.

    Args:
        contract_path: Path to Cairo file or project directory
        detectors: Optional comma-separated detector names
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with:
        - summary: Parsed findings (by severity, detector type)
        - outputFile: Path to raw caracal output
        - message: Human-readable summary
    """

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_name = re.sub(r'[^\w\-]', '_', contract_path.split('/')[-1])
    filename = f"{safe_name}-{timestamp}.txt"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "caracal"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "caracal"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command
    cmd = f"caracal detect {contract_path}"
    if detectors:
        cmd += f" --detectors {detectors}"

    try:
        result = docker_exec("web3-security", cmd, timeout=300)

        # Save raw output
        output_file.write_text(result["stdout"] + result["stderr"], encoding='utf-8')

        # Parse the output
        summary = parse_caracal_output(result["stdout"] + result["stderr"])

        # Generate message
        total = summary["totalIssues"]
        message = f"[+] Caracal analysis complete\n"
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
                message += f"      [{issue['severity']}] {issue['detector']}: {issue['description'][:80]}...\n"

        message += f"    Full results: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Caracal timed out (5 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"Caracal execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def caracal_print(contract_path: str, printer: str = "cfg", engagement_dir: Optional[str] = None) -> Dict:
    """
    Generate Caracal visualizations (CFG, call graphs, etc.).

    Args:
        contract_path: Path to Cairo file or project directory
        printer: Type of output (cfg, call-graph, function-summary)
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with outputFile path and message
    """

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_name = re.sub(r'[^\w\-]', '_', contract_path.split('/')[-1])
    filename = f"{safe_name}-{printer}-{timestamp}.txt"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "caracal" / "visualizations"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "caracal" / "visualizations"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command
    cmd = f"caracal print {contract_path} --printer {printer}"

    try:
        result = docker_exec("web3-security", cmd, timeout=300)

        # Save raw output
        output_file.write_text(result["stdout"] + result["stderr"], encoding='utf-8')

        message = f"[+] Caracal visualization complete\n"
        message += f"    Target: {contract_path}\n"
        message += f"    Printer: {printer}\n"
        message += f"    Output: {output_file}\n"

        # Check for .dot files (graphs)
        dot_files = list(output_dir.glob("*.dot"))
        if dot_files:
            message += f"    Graph files: {len(dot_files)} .dot files generated"

        return {
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Caracal timed out (5 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"Caracal execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def parse_caracal_output(output: str) -> Dict:
    """Parse Caracal text output."""

    # Caracal outputs in text format with severity markers
    # Example: [High] Reentrancy in function transfer()
    #          [Medium] Unchecked transfer in function mint()

    by_severity = {}
    by_detector = {}
    top_issues = []

    lines = output.split('\n')
    for line in lines:
        # Match severity and detector patterns
        match = re.match(r'\[(High|Medium|Low|Informational)\]\s+([^:]+):\s*(.*)', line)
        if match:
            severity = match.group(1)
            detector = match.group(2).strip()
            description = match.group(3).strip()

            # Count by severity
            by_severity[severity] = by_severity.get(severity, 0) + 1

            # Count by detector
            by_detector[detector] = by_detector.get(detector, 0) + 1

            # Collect top issues
            top_issues.append({
                "severity": severity,
                "detector": detector,
                "description": description
            })

    return {
        "totalIssues": len(top_issues),
        "bySeverity": by_severity,
        "byDetector": by_detector,
        "topIssues": top_issues[:20]  # Top 20
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Detection: python caracal.py detect <contract_path> [detectors] [engagement_dir]")
        print("  Visualize: python caracal.py print <contract_path> [printer] [engagement_dir]")
        print("")
        print("Examples:")
        print("  python caracal.py detect contract.cairo")
        print("  python caracal.py detect project/ 'reentrancy,unchecked-transfer'")
        print("  python caracal.py print contract.cairo cfg")
        print("  python caracal.py print contract.cairo call-graph")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "detect":
        contract_path = sys.argv[2] if len(sys.argv) > 2 else ""
        detectors = sys.argv[3] if len(sys.argv) > 3 else ""
        engagement_dir = sys.argv[4] if len(sys.argv) > 4 else None

        if not contract_path:
            print("[!] Error: contract_path required")
            sys.exit(1)

        result = caracal_detect(contract_path, detectors, engagement_dir)

    elif mode == "print":
        contract_path = sys.argv[2] if len(sys.argv) > 2 else ""
        printer = sys.argv[3] if len(sys.argv) > 3 else "cfg"
        engagement_dir = sys.argv[4] if len(sys.argv) > 4 else None

        if not contract_path:
            print("[!] Error: contract_path required")
            sys.exit(1)

        result = caracal_print(contract_path, printer, engagement_dir)

    else:
        print(f"[!] Error: Unknown mode '{mode}'. Use 'detect' or 'print'")
        sys.exit(1)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
