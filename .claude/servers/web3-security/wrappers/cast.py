#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cast wrapper - MCP Code API Pattern (VPS Docker deployment)
Foundry cast utilities for blockchain interaction
"""

import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def cast_call(contract_address: str, function_signature: str, rpc_url: str, engagement_dir: Optional[str] = None) -> Dict:
    """Execute read-only contract function call."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"cast-call-{contract_address[:8]}-{timestamp}.txt"

    if engagement_dir:
        output_dir = Path(engagement_dir) / "02-reconnaissance" / "cast"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "cast"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    cmd = f"cast call {contract_address} '{function_signature}' --rpc-url {rpc_url}"

    try:
        result = docker_exec("web3-security", cmd, timeout=60)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["stdout"] + result["stderr"])

        message = f"[+] cast call complete\n    Contract: {contract_address}\n    Function: {function_signature}\n    Result: {result["stdout"].strip()}\n    Full output: {output_file}"

        return {"summary": {"result": result["stdout"].strip()}, "outputFile": str(output_file), "message": message}
    except subprocess.TimeoutExpired:
        return {"error": "cast call timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": f"cast call error: {str(e)}", "outputFile": str(output_file)}


def cast_storage(contract_address: str, storage_slot: str, rpc_url: str, engagement_dir: Optional[str] = None) -> Dict:
    """Read contract storage slot value."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"cast-storage-{contract_address[:8]}-slot{storage_slot}-{timestamp}.txt"

    if engagement_dir:
        output_dir = Path(engagement_dir) / "02-reconnaissance" / "cast"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "scans" / "cast"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    cmd = f"cast storage {contract_address} {storage_slot} --rpc-url {rpc_url}"

    try:
        result = docker_exec("web3-security", cmd, timeout=60)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["stdout"] + result["stderr"])

        message = f"[+] cast storage complete\n    Contract: {contract_address}\n    Slot: {storage_slot}\n    Value: {result["stdout"].strip()}\n    Full output: {output_file}"

        return {"summary": {"value": result["stdout"].strip()}, "outputFile": str(output_file), "message": message}
    except subprocess.TimeoutExpired:
        return {"error": "cast storage timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": f"cast storage error: {str(e)}", "outputFile": str(output_file)}


def cast_abi_decode(data_type: str, calldata: str, engagement_dir: Optional[str] = None) -> Dict:
    """Decode ABI-encoded data."""
    cmd = f"cast abi-decode '{data_type}' {calldata}"

    try:
        result = docker_exec("web3-security", cmd, timeout=30)
        message = f"[+] ABI decode complete\n    Type: {data_type}\n    Result: {result["stdout"].strip()}"
        return {"summary": {"decoded": result["stdout"].strip()}, "message": message}
    except Exception as e:
        return {"error": f"cast abi-decode error: {str(e)}"}


def cast_4byte(signature: str, engagement_dir: Optional[str] = None) -> Dict:
    """Get function signature from 4byte selector."""
    cmd = f"cast 4byte {signature}"

    try:
        result = docker_exec("web3-security", cmd, timeout=30)
        message = f"[+] 4byte lookup complete\n    Selector: {signature}\n    Signatures: {result["stdout"].strip()}"
        return {"summary": {"signatures": result["stdout"].strip()}, "message": message}
    except Exception as e:
        return {"error": f"cast 4byte error: {str(e)}"}


def cast_4byte_decode(calldata: str, engagement_dir: Optional[str] = None) -> Dict:
    """Decode calldata using 4byte directory."""
    cmd = f"cast 4byte-decode {calldata}"

    try:
        result = docker_exec("web3-security", cmd, timeout=30)
        message = f"[+] 4byte decode complete\n    Calldata: {calldata[:20]}...\n    Decoded: {result["stdout"].strip()}"
        return {"summary": {"decoded": result["stdout"].strip()}, "message": message}
    except Exception as e:
        return {"error": f"cast 4byte-decode error: {str(e)}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cast.py <function> <args...>")
        print("Functions: call, storage, abi_decode, 4byte, 4byte_decode")
        sys.exit(1)

    func = sys.argv[1]
    if func == "call" and len(sys.argv) >= 5:
        result = cast_call(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    elif func == "storage" and len(sys.argv) >= 5:
        result = cast_storage(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    elif func == "abi_decode" and len(sys.argv) >= 4:
        result = cast_abi_decode(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif func == "4byte" and len(sys.argv) >= 3:
        result = cast_4byte(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif func == "4byte_decode" and len(sys.argv) >= 3:
        result = cast_4byte_decode(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print("Invalid function or missing arguments")
        sys.exit(1)

    print(result.get("error") or result["message"])
