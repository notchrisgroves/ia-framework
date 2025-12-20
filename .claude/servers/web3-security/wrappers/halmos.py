#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""halmos wrapper - MCP Code API Pattern (VPS Docker deployment)"""
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

def halmos(contract_path: str, function_name: str = "", solver_timeout: str = "300", engagement_dir: Optional[str] = None) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{Path(contract_path).name}-{timestamp}.txt"
    
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "halmos"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "halmos"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    
    cmd = f"halmos --root {contract_path} --solver-timeout-assertion {solver_timeout}"
    if function_name:
        cmd += f" --function {function_name}"
    cmd += f" > {output_file} 2>&1"
    
    try:
        subprocess.run(cmd, shell=True, timeout=int(solver_timeout) + 60)
        if not output_file.exists():
            return {"error": "halmos failed", "outputFile": str(output_file)}
        
        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        passed = content.count('[PASS]')
        failed = content.count('[FAIL]')
        
        message = f"[+] halmos verification complete\n    Target: {contract_path}\n    Passed: {passed}\n    Failed: {failed}\n    Full results: {output_file}"
        
        return {"summary": {"passed": passed, "failed": failed}, "outputFile": str(output_file), "message": message}
    except subprocess.TimeoutExpired:
        return {"error": f"halmos timed out ({solver_timeout}s)", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": f"halmos error: {str(e)}", "outputFile": str(output_file)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python halmos.py <contract_path> [function] [timeout] [engagement_dir]")
        sys.exit(1)
    result = halmos(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "", sys.argv[3] if len(sys.argv) > 3 else "300", sys.argv[4] if len(sys.argv) > 4 else None)
    print(result.get("error") or result["message"])
