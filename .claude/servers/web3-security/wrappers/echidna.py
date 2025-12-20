#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""echidna wrapper - MCP Code API Pattern (VPS Docker deployment)"""
import sys, io, subprocess, json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def echidna(contract_path: str, config_file: str = "", timeout: str = "300", engagement_dir: Optional[str] = None) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{Path(contract_path).stem}-{timestamp}.txt"
    
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "echidna"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "echidna"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    
    cmd = f"echidna {contract_path} --test-mode assertion --timeout {timeout}"
    if config_file:
        cmd += f" --config {config_file}"
    cmd += f" > {output_file} 2>&1"
    
    try:
        subprocess.run(cmd, shell=True, timeout=int(timeout) + 30)
        if not output_file.exists():
            return {"error": "echidna failed", "outputFile": str(output_file)}
        
        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        passed = content.count('passed')
        failed = content.count('failed')
        
        message = f"[+] echidna fuzzing complete\n    Target: {contract_path}\n    Tests passed: {passed}\n    Tests failed: {failed}\n    Full results: {output_file}"
        
        return {"summary": {"passed": passed, "failed": failed}, "outputFile": str(output_file), "message": message}
    except subprocess.TimeoutExpired:
        return {"error": f"echidna timed out ({timeout}s)", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": f"echidna error: {str(e)}", "outputFile": str(output_file)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python echidna.py <contract_path> [config] [timeout] [engagement_dir]")
        sys.exit(1)
    result = echidna(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "", sys.argv[3] if len(sys.argv) > 3 else "300", sys.argv[4] if len(sys.argv) > 4 else None)
    print(result.get("error") or result["message"])
