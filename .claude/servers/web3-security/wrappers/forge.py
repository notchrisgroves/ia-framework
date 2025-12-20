#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""forge wrapper - Foundry testing and coverage"""
import sys, io, subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def forge_test(project_path: str, match_test: str = "", gas_report: str = "false", engagement_dir: Optional[str] = None) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"forge-test-{timestamp}.txt"
    
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "forge"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "forge"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    
    cmd = f"cd {project_path} && forge test"
    if match_test:
        cmd += f" --match-test {match_test}"
    if gas_report == "true":
        cmd += " --gas-report"
    cmd += f" > {output_file} 2>&1"
    
    try:
        subprocess.run(cmd, shell=True, timeout=300)
        message = f"[+] forge test complete\n    Project: {project_path}\n    Full output: {output_file}"
        return {"summary": {"tested": True}, "outputFile": str(output_file), "message": message}
    except Exception as e:
        return {"error": f"forge test error: {str(e)}", "outputFile": str(output_file)}

def forge_coverage(project_path: str, report_file: str = "", engagement_dir: Optional[str] = None) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = report_file or f"coverage-{timestamp}.lcov"
    
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "forge"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "forge"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    
    cmd = f"cd {project_path} && forge coverage --report lcov > {output_file} 2>&1"
    
    try:
        subprocess.run(cmd, shell=True, timeout=300)
        message = f"[+] forge coverage complete\n    Project: {project_path}\n    Report: {output_file}"
        return {"summary": {"coverage": True}, "outputFile": str(output_file), "message": message}
    except Exception as e:
        return {"error": f"forge coverage error: {str(e)}", "outputFile": str(output_file)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python forge.py <test|coverage> <project_path> [args...]")
        sys.exit(1)
    func, path = sys.argv[1], sys.argv[2]
    if func == "test":
        result = forge_test(path, sys.argv[3] if len(sys.argv) > 3 else "", sys.argv[4] if len(sys.argv) > 4 else "false", sys.argv[5] if len(sys.argv) > 5 else None)
    elif func == "coverage":
        result = forge_coverage(path, sys.argv[3] if len(sys.argv) > 3 else "", sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        sys.exit(1)
    print(result.get("error") or result["message"])
