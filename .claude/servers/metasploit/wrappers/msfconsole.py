#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Metasploit Framework msfconsole - VPS Docker Wrapper
=====================================================

VPS Code API Pattern: SSH + docker exec + file storage

Token Optimization:
- Saves full output to local file
- Returns minimal summary (commands run, status)
- File storage enables 95% token reduction

Author: Intelligence Adjacent Framework
Date: 2025-11-16
"""

import sys
import io
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    # Only wrap if not already wrapped
    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if not isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# VPS Configuration
VPS_HOST = "15.204.218.153"
VPS_PORT = "2222"
VPS_USER = "debian"
SSH_KEY = Path.home() / ".ssh" / "gro_256"
CONTAINER_NAME = "metasploit"
OUTPUT_DIR = Path.home() / ".claude" / "cache" / "metasploit"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _docker_exec(command: str, output_file: Optional[Path] = None) -> Dict:
    """
    Execute command in Metasploit container via SSH + docker exec.

    Args:
        command: Command to run inside container
        output_file: Optional file path to save full output

    Returns:
        Dict with status, summary, and output_file path
    """
    # Build SSH command
    ssh_cmd = [
        "ssh",
        "-i", str(SSH_KEY),
        "-p", VPS_PORT,
        f"{VPS_USER}@{VPS_HOST}",
        f"docker exec {CONTAINER_NAME} {command}"
    ]

    try:
        # Execute command
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        # Save full output to file if specified
        if output_file:
            output_file.write_text(result.stdout + result.stderr)

        # Return minimal summary
        return {
            "status": "success" if result.returncode == 0 else "error",
            "returnCode": result.returncode,
            "outputLines": len(result.stdout.splitlines()),
            "errorLines": len(result.stderr.splitlines()),
            "outputFile": str(output_file) if output_file else None,
            "preview": result.stdout[:200] if result.stdout else result.stderr[:200]
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "error": "Command execution timed out after 5 minutes",
            "outputFile": str(output_file) if output_file else None
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "outputFile": str(output_file) if output_file else None
        }


def version() -> Dict:
    """
    Get Metasploit Framework version.

    Returns:
        Version information

    Example:
        >>> from servers.metasploit import msfconsole
        >>> msfconsole.version()
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"version_{timestamp}.txt"

    return _docker_exec("msfconsole --version", output_file)


def test_connection() -> Dict:
    """
    Test connectivity to Metasploit container.

    Returns:
        Connection status and version info

    Example:
        >>> from servers.metasploit import msfconsole
        >>> msfconsole.test_connection()
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"test_connection_{timestamp}.txt"

    result = _docker_exec("msfconsole --version", output_file)

    if result["status"] == "success":
        result["message"] = "[+] Metasploit container is accessible via Twingate"
    else:
        result["message"] = "[-] Failed to connect to Metasploit container"

    return result


def search_modules(keyword: str, detail_level: str = "minimal") -> Dict:
    """
    Search for Metasploit modules.

    Args:
        keyword: Search term (e.g., "eternalblue", "smb", "apache")
        detail_level: "minimal" (counts only), "standard" (top 10), "full" (all results)

    Returns:
        Search results with module count and matches

    Example:
        >>> from servers.metasploit import msfconsole
        >>> msfconsole.search_modules("ms17-010")
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"search_{keyword}_{timestamp}.txt"

    # Build msfconsole command
    command = f'msfconsole -q -x "search {keyword}; exit"'

    result = _docker_exec(command, output_file)

    if result["status"] == "success" and output_file.exists():
        full_output = output_file.read_text()
        lines = [l for l in full_output.splitlines() if l.strip()]

        # Count module matches
        module_lines = [l for l in lines if "/" in l and not l.startswith("msf")]

        result["moduleCount"] = len(module_lines)

        if detail_level == "minimal":
            result["modules"] = module_lines[:5] if len(module_lines) > 5 else module_lines
        elif detail_level == "standard":
            result["modules"] = module_lines[:10]
        else:  # full
            result["modules"] = "See outputFile for full results"

    return result


def run_command(commands: List[str], detail_level: str = "minimal") -> Dict:
    """
    Run Metasploit console commands.

    Args:
        commands: List of msfconsole commands to execute
        detail_level: "minimal" (summary only), "standard" (first 20 lines), "full" (see file)

    Returns:
        Command execution results

    Example:
        >>> from servers.metasploit import msfconsole
        >>> msfconsole.run_command(["db_status", "version"])
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"commands_{timestamp}.txt"

    # Build command string
    cmd_string = "; ".join(commands) + "; exit"
    command = f'msfconsole -q -x "{cmd_string}"'

    result = _docker_exec(command, output_file)

    if result["status"] == "success" and output_file.exists():
        full_output = output_file.read_text()
        lines = full_output.splitlines()

        result["commandCount"] = len(commands)

        if detail_level == "minimal":
            result["output"] = f"{len(lines)} lines of output - see outputFile"
        elif detail_level == "standard":
            result["output"] = lines[:20]
        # full: user reads outputFile directly

    return result


def db_status() -> Dict:
    """
    Check Metasploit database status.

    Returns:
        Database connection status

    Example:
        >>> from servers.metasploit import msfconsole
        >>> msfconsole.db_status()
    """
    return run_command(["db_status"], detail_level="standard")


# CLI Testing
if __name__ == "__main__":
    print("[*] Testing Metasploit connection...")
    result = test_connection()
    print(f"Status: {result['status']}")
    print(f"Message: {result.get('message', 'No message')}")

    if result["status"] == "success":
        print(f"\n[*] Preview:")
        print(result.get("preview", "No preview"))
        print(f"\n[*] Full output saved to: {result['outputFile']}")
