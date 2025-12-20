#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""frida wrapper - Dynamic instrumentation for mobile apps"""
import sys
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def frida_ps(
    device_id: Optional[str] = None,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    List running processes on connected device using frida-ps.

    Token efficiency:
    - Minimal mode: ~50 tokens (process count, sample names)
    - Standard mode: ~150 tokens (process list with PIDs)
    - Full mode: ~400 tokens (complete process list with metadata)
    - No caching (dynamic process list)

    Args:
        device_id: Optional device identifier (USB, emulator)
        engagement_dir: Optional engagement directory
        detail_level: "minimal" | "standard" | "full"

    Returns:
        Dict with summary, outputFile, and message
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    # Determine output location
    if engagement_dir:
        output_dir = Path(engagement_dir) / "04-analysis" / "frida"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "frida"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"processes-{timestamp}.json"

    # Build frida-ps command
    cmd = ["docker", "run", "--rm", "--net=host", "mobile-tools-mcp-server", "frida-ps"]
    if device_id:
        cmd.extend(["-D", device_id])
    cmd.append("-j")  # JSON output

    # Execute frida-ps
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse JSON output
        try:
            processes = json.loads(result["stdout"]) if result["stdout"] else []
        except json.JSONDecodeError:
            processes = []

        # Save full output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processes, f, indent=2)

        # Parse process list
        summary = _parse_processes(processes, detail_level)

        message = f"[+] Frida process list retrieved\n"
        message += f"    Device: {device_id or 'default'}\n"
        message += f"    Processes: {summary.get('processCount', 0)}\n"
        message += f"    Full list: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "frida-ps timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": str(e), "outputFile": str(output_file)}

def _parse_processes(processes: list, detail_level: str) -> Dict:
    """Parse frida process list."""
    if not processes:
        return {"processCount": 0}

    # Minimal: Just count and sample names
    if detail_level == "minimal":
        sample_names = [p.get("name", "unknown") for p in processes[:5]]
        return {
            "processCount": len(processes),
            "sampleProcesses": sample_names
        }

    # Standard: Process list with PIDs
    elif detail_level == "standard":
        process_list = [
            {"name": p.get("name", "unknown"), "pid": p.get("pid")}
            for p in processes[:20]
        ]
        return {
            "processCount": len(processes),
            "processes": process_list
        }

    # Full: Complete process information
    else:
        return {
            "processCount": len(processes),
            "processes": processes
        }

if __name__ == "__main__":
    result = frida_ps(device_id=sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps(result, indent=2))
