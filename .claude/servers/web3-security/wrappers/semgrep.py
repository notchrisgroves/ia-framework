#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semgrep wrapper - MCP Code API Pattern (VPS Docker deployment)
Executes semgrep, saves raw output, returns parsed summary
"""

import sys
import io
import json
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


def semgrep(contract_path: str, rules: str = "p/smart-contracts", output_format: str = "text", engagement_dir: Optional[str] = None) -> Dict:
    """Execute semgrep pattern-based analysis."""

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_name = Path(contract_path).name.replace(".", "_")
    ext = "json" if output_format == "json" else "txt"
    filename = f"{safe_name}-{timestamp}.{ext}"

    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "semgrep"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "semgrep"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    cmd = f"semgrep --config {rules} {contract_path} --{output_format} -o {output_file}"

    try:
        subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)

        if not output_file.exists():
            return {"error": "semgrep execution failed", "outputFile": str(output_file)}

        summary = parse_semgrep_output(output_file, output_format)

        message = f"[+] semgrep analysis complete\n"
        message += f"    Target: {contract_path}\n"
        message += f"    Findings: {summary['totalFindings']}\n"

        if summary["bySeverity"]:
            message += f"    By severity:\n"
            for sev in ['ERROR', 'WARNING', 'INFO']:
                if sev in summary["bySeverity"]:
                    message += f"      {sev}: {summary['bySeverity'][sev]}\n"

        message += f"    Full results: {output_file}"

        return {"summary": summary, "outputFile": str(output_file), "message": message}

    except subprocess.TimeoutExpired:
        return {"error": "semgrep timed out (5 minutes)", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": f"semgrep execution error: {str(e)}", "outputFile": str(output_file)}


def parse_semgrep_output(filepath: Path, format_type: str) -> Dict:
    """Parse semgrep output file."""

    if not filepath.exists():
        return {"totalFindings": 0, "bySeverity": {}, "topFindings": []}

    if format_type == "json":
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            results = data.get('results', [])
            by_severity = {}
            for r in results:
                sev = r.get('extra', {}).get('severity', 'INFO')
                by_severity[sev] = by_severity.get(sev, 0) + 1
            return {"totalFindings": len(results), "bySeverity": by_severity, "topFindings": results[:20]}
        except:
            return {"totalFindings": 0, "bySeverity": {}, "topFindings": []}
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        findings = content.count('rule:')
        return {"totalFindings": findings, "bySeverity": {}, "topFindings": []}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python semgrep.py <contract_path> [rules] [format] [engagement_dir]")
        sys.exit(1)

    contract_path = sys.argv[1]
    rules = sys.argv[2] if len(sys.argv) > 2 else "p/smart-contracts"
    output_format = sys.argv[3] if len(sys.argv) > 3 else "text"
    engagement_dir = sys.argv[4] if len(sys.argv) > 4 else None

    result = semgrep(contract_path, rules, output_format, engagement_dir)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
