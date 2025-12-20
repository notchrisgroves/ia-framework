#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brownie wrapper - Smart contract compilation"""
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

def brownie_compile(project_path: str, engagement_dir: Optional[str] = None) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"brownie-compile-{timestamp}.txt"
    
    if engagement_dir:
        output_dir = Path(engagement_dir) / "01-planning" / "compilation"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "brownie"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    
    cmd = f"cd {project_path} && brownie compile > {output_file} 2>&1"
    
    try:
        subprocess.run(cmd, shell=True, timeout=300)
        message = f"[+] brownie compile complete\n    Project: {project_path}\n    Full output: {output_file}"
        return {"summary": {"compiled": True}, "outputFile": str(output_file), "message": message}
    except subprocess.TimeoutExpired:
        return {"error": "brownie compile timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": f"brownie compile error: {str(e)}", "outputFile": str(output_file)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brownie.py <project_path> [engagement_dir]")
        sys.exit(1)
    result = brownie_compile(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(result.get("error") or result["message"])
