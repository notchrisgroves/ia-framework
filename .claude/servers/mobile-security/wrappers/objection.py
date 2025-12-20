#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""objection wrapper - Mobile app security testing and exploration"""
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def objection_explore(
    app_identifier: str,
    command: Optional[str] = None,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Start objection exploration session for mobile app security testing.

    Token efficiency:
    - Minimal mode: ~80 tokens (session status, app info)
    - Standard mode: ~200 tokens (environment details)
    - Full mode: ~500 tokens (complete session info)
    - No caching (dynamic session data)

    Args:
        app_identifier: Application package name or bundle ID
        command: Optional objection command to execute
        engagement_dir: Optional engagement directory
        detail_level: "minimal" | "standard" | "full"

    Returns:
        Dict with summary, outputFile, and message

    Note: For interactive sessions, use objection directly.
    This wrapper is for command execution only.
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    # Determine output location
    if engagement_dir:
        output_dir = Path(engagement_dir) / "04-analysis" / "objection"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "objection"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{app_identifier.replace('.', '_')}-{timestamp}.txt"

    # Build objection command
    cmd = ["docker", "run", "--rm", "--net=host", "mobile-tools-mcp-server", "objection"]
    cmd.extend(["-g", app_identifier])

    if command:
        cmd.extend(["-c", command])
    else:
        # Default: get app info
        cmd.extend(["-c", "env"])

    # Execute objection
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Save full output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["stdout"])
            if result["stderr"]:
                f.write("\n\n=== STDERR ===\n")
                f.write(result["stderr"])

        # Parse output
        summary = _parse_objection_output(result["stdout"], command, detail_level)

        message = f"[+] Objection command executed\n"
        message += f"    App: {app_identifier}\n"
        message += f"    Command: {command or 'env'}\n"
        message += f"    Full output: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "objection command timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": str(e), "outputFile": str(output_file)}

def _parse_objection_output(output: str, command: Optional[str], detail_level: str) -> Dict:
    """Parse objection command output."""
    lines = output.split('\n')

    # Minimal: Basic status
    if detail_level == "minimal":
        return {
            "command": command or "env",
            "lineCount": len(lines),
            "success": "error" not in output.lower()
        }

    # Standard: Add key info
    elif detail_level == "standard":
        # Extract key environment info if env command
        info = {}
        if not command or command == "env":
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip()] = value.strip()

        return {
            "command": command or "env",
            "lineCount": len(lines),
            "success": "error" not in output.lower(),
            "info": info if info else None,
            "preview": '\n'.join(lines[:10])
        }

    # Full: Complete output
    else:
        return {
            "command": command or "env",
            "lineCount": len(lines),
            "success": "error" not in output.lower(),
            "output": output[:2000]  # First 2000 chars
        }

if __name__ == "__main__":
    import json
    result = objection_explore(
        app_identifier=sys.argv[1] if len(sys.argv) > 1 else "com.example.app",
        command=sys.argv[2] if len(sys.argv) > 2 else None
    )
    print(json.dumps(result, indent=2))
