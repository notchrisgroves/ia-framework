#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VPS Utilities - Common functions for SSH + Docker exec
Loads VPS configuration from .env and provides reusable SSH wrappers

SETUP REQUIRED:
1. Configure .env with your VPS credentials (see .env.example)
2. Ensure SSH key authentication is set up on your VPS
3. Run: python servers/utils/vps_utils.py to test connection

Environment Variables (.env):
- VPS_HOST: IP address or hostname of your VPS
- VPS_USER: SSH username (e.g., 'debian', 'ubuntu', 'root')
- VPS_SSH_KEY: Path to SSH private key
- VPS_SSH_PORT: SSH port (default: 22)
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

# Load .env from Claude root (override=True to prioritize .env over system variables like USERNAME)
env_path = Path.home() / ".claude" / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)

# VPS Configuration from .env - NO DEFAULTS (requires user configuration)
VPS_HOST = os.getenv("VPS_HOST", "")
VPS_USER = os.getenv("VPS_USER", "")
VPS_SSH_KEY = os.getenv("VPS_SSH_KEY", "")
VPS_SSH_PORT = os.getenv("VPS_SSH_PORT", "22")

# Legacy variable support (for backwards compatibility)
if not VPS_HOST:
    VPS_HOST = os.getenv("IPv4_address", "")
if not VPS_USER:
    VPS_USER = os.getenv("Username", "")
if not VPS_SSH_KEY:
    VPS_SSH_KEY = os.getenv("SSH_PRIV", "")

# Container mappings - standard container names
CONTAINER_MAP = {
    "kali-pentest": "kali-pentest",
    "web3-security": "web3-security",
    "mobile-tools": "mobile-tools",
    "reaper": "reaper",
    "metasploit": "metasploit",
    "playwright": "playwright"
}


def is_configured() -> bool:
    """Check if VPS is configured in .env."""
    return bool(VPS_HOST and VPS_USER and VPS_SSH_KEY)


def get_configuration_status() -> Dict:
    """Get detailed configuration status for troubleshooting."""
    return {
        "configured": is_configured(),
        "vps_host": bool(VPS_HOST),
        "vps_user": bool(VPS_USER),
        "vps_ssh_key": bool(VPS_SSH_KEY),
        "ssh_key_exists": Path(VPS_SSH_KEY).exists() if VPS_SSH_KEY else False,
        "env_file_exists": env_path.exists(),
        "message": _get_config_message()
    }


def _get_config_message() -> str:
    """Generate helpful configuration message."""
    if is_configured():
        if not Path(VPS_SSH_KEY).exists():
            return f"SSH key not found at: {VPS_SSH_KEY}"
        return "VPS configured and ready"

    missing = []
    if not VPS_HOST:
        missing.append("VPS_HOST")
    if not VPS_USER:
        missing.append("VPS_USER")
    if not VPS_SSH_KEY:
        missing.append("VPS_SSH_KEY")

    return f"Missing .env variables: {', '.join(missing)}. See servers/SETUP-GUIDE.md"


def docker_exec(container: str, command: str, timeout: int = 300) -> Dict:
    """
    Execute command in Docker container on VPS via SSH.

    Args:
        container: Container name (kali-pentest, web3-security, mobile-tools, reaper)
        command: Command to execute inside container
        timeout: Timeout in seconds (default: 300)

    Returns:
        Dict with:
        - returncode: Exit code
        - stdout: Standard output
        - stderr: Standard error
    """
    # Check configuration first
    if not is_configured():
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": _get_config_message()
        }

    if container not in CONTAINER_MAP:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": f"Unknown container: {container}. Valid: {list(CONTAINER_MAP.keys())}"
        }

    # Build SSH + docker exec command (list format for Windows compatibility)
    ssh_cmd = [
        "ssh",
        "-i", VPS_SSH_KEY,
        "-p", VPS_SSH_PORT,
        f"{VPS_USER}@{VPS_HOST}",
        f"docker exec {container} {command}"
    ]

    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "returncode": 124,  # Standard timeout exit code
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": f"Execution error: {str(e)}"
        }


def vps_ssh(command: str, timeout: int = 60) -> Dict:
    """
    Execute command directly on VPS (not in container).

    Args:
        command: Shell command to execute on VPS
        timeout: Timeout in seconds (default: 60)

    Returns:
        Dict with returncode, stdout, stderr
    """
    # Check configuration first
    if not is_configured():
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": _get_config_message()
        }

    # Build SSH command (list format for Windows compatibility)
    ssh_cmd = [
        "ssh",
        "-i", VPS_SSH_KEY,
        "-p", VPS_SSH_PORT,
        f"{VPS_USER}@{VPS_HOST}",
        command
    ]

    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "returncode": 124,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": f"Execution error: {str(e)}"
        }


def get_vps_config() -> Dict[str, str]:
    """
    Get VPS configuration details.

    Returns:
        Dict with host, user, ssh_key
    """
    return {
        "host": VPS_HOST,
        "user": VPS_USER,
        "ssh_key": VPS_SSH_KEY,
        "containers": list(CONTAINER_MAP.keys())
    }


def test_vps_connection() -> bool:
    """
    Test VPS SSH connectivity.

    Returns:
        True if connection successful, False otherwise
    """
    result = vps_ssh("echo 'test'", timeout=10)
    return result["returncode"] == 0 and "test" in result["stdout"]


def test_container(container: str) -> bool:
    """
    Test if container is running and accessible.

    Args:
        container: Container name

    Returns:
        True if container accessible, False otherwise
    """
    result = docker_exec(container, "echo 'test'", timeout=10)
    return result["returncode"] == 0 and "test" in result["stdout"]


if __name__ == "__main__":
    # CLI testing
    import sys

    print("VPS Configuration:")
    config = get_vps_config()
    for key, value in config.items():
        print(f"  {key}: {value}")

    print("\nTesting VPS connection...")
    if test_vps_connection():
        print("  ✓ VPS connection successful")
    else:
        print("  ✗ VPS connection failed")
        sys.exit(1)

    print("\nTesting containers...")
    for container in CONTAINER_MAP.keys():
        if test_container(container):
            print(f"  ✓ {container} accessible")
        else:
            print(f"  ✗ {container} not accessible")
