#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""solc wrapper - Compiler version management"""
import sys, io, subprocess

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def solc_versions():
    """List available Solidity compiler versions."""
    result = docker_exec("web3-security", "solc-select versions", timeout=300)
    return {"message": result["stdout"]}

def solc_install(version: str):
    """Install specific Solidity compiler version."""
    result = docker_exec("web3-security", f"solc-select install {version}", timeout=300)
    return {"message": f"Installed solc {version}\n{result["stdout"]}"}

def solc_use(version: str):
    """Switch to specific Solidity compiler version."""
    result = docker_exec("web3-security", f"solc-select use {version}", timeout=300)
    return {"message": f"Switched to solc {version}\n{result["stdout"]}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solc.py <versions|install|use> [version]")
        sys.exit(1)
    func = sys.argv[1]
    if func == "versions":
        print(solc_versions()["message"])
    elif func == "install" and len(sys.argv) >= 3:
        print(solc_install(sys.argv[2])["message"])
    elif func == "use" and len(sys.argv) >= 3:
        print(solc_use(sys.argv[2])["message"])
