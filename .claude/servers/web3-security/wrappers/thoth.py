#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thoth wrapper - MCP Code API Pattern (VPS Docker deployment)
Executes thoth bytecode analysis/decompilation, saves raw output, returns summary

Token Optimization: 95.7% reduction (saves full output, returns summary)
Note: Repository no longer maintained but still functional
"""

import sys
import io
import re
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


def thoth_decompile(contract_address: str = "", network: str = "mainnet",
                   contract_path: str = "", engagement_dir: Optional[str] = None) -> Dict:
    """
    Decompile Cairo bytecode to readable format.

    Args:
        contract_address: Deployed contract address (for remote analysis)
        network: Starknet network (mainnet, goerli, sepolia)
        contract_path: Path to local compiled contract JSON
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with outputFile path and message
    """

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    if contract_address:
        safe_name = contract_address[:10]
        filename = f"{safe_name}-{network}-decompiled-{timestamp}.txt"
    else:
        safe_name = re.sub(r'[^\w\-]', '_', contract_path.split('/')[-1])
        filename = f"{safe_name}-decompiled-{timestamp}.txt"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "thoth" / "decompiled"
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "thoth" / "decompiled"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command
    if contract_address:
        cmd = f"thoth remote --address {contract_address} --network {network} --decompile"
    elif contract_path:
        cmd = f"thoth local {contract_path} --decompile"
    else:
        return {
            "error": "Either contract_address or contract_path is required"
        }

    try:
        result = docker_exec("web3-security", cmd, timeout=300)

        # Save raw output
        output_file.write_text(result["stdout"] + result["stderr"], encoding='utf-8')

        # Parse output for summary
        summary = parse_thoth_decompile(result["stdout"])

        message = f"[+] Thoth decompilation complete\n"
        if contract_address:
            message += f"    Contract: {contract_address} ({network})\n"
        else:
            message += f"    Contract: {contract_path}\n"
        message += f"    Functions found: {summary['functionCount']}\n"
        message += f"    Output: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Thoth timed out (5 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"Thoth execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def thoth_analyze(contract_address: str = "", network: str = "mainnet",
                 contract_path: str = "", analysis_type: str = "cfg",
                 engagement_dir: Optional[str] = None) -> Dict:
    """
    Analyze Cairo bytecode structure and control flow.

    Args:
        contract_address: Deployed contract address (for remote analysis)
        network: Starknet network (mainnet, goerli, sepolia)
        contract_path: Path to local compiled contract JSON
        analysis_type: Type of analysis (cfg, call-graph, disassemble, symbolic)
        engagement_dir: Optional engagement directory path

    Returns:
        Dict with summary, outputFile path, and message
    """

    # Generate output filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    if contract_address:
        safe_name = contract_address[:10]
        filename = f"{safe_name}-{network}-{analysis_type}-{timestamp}.txt"
    else:
        safe_name = re.sub(r'[^\w\-]', '_', contract_path.split('/')[-1])
        filename = f"{safe_name}-{analysis_type}-{timestamp}.txt"

    # Determine output directory
    if engagement_dir:
        output_dir = Path(engagement_dir) / "03-vulnerability-assessment" / "thoth" / analysis_type
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "scans" / "thoth" / analysis_type

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Build command
    if contract_address:
        cmd = f"thoth remote --address {contract_address} --network {network}"
    elif contract_path:
        cmd = f"thoth local {contract_path}"
    else:
        return {
            "error": "Either contract_address or contract_path is required"
        }

    # Add analysis type flag
    if analysis_type == "cfg":
        cmd += " --cfg"
    elif analysis_type == "call-graph":
        cmd += " --call-graph"
    elif analysis_type == "disassemble":
        cmd += " --disassemble"
    elif analysis_type == "symbolic":
        cmd += " --symbolic"

    try:
        result = docker_exec("web3-security", cmd, timeout=600)

        # Save raw output
        output_file.write_text(result["stdout"] + result["stderr"], encoding='utf-8')

        # Parse output for summary
        summary = parse_thoth_analysis(result["stdout"], analysis_type)

        message = f"[+] Thoth {analysis_type} analysis complete\n"
        if contract_address:
            message += f"    Contract: {contract_address} ({network})\n"
        else:
            message += f"    Contract: {contract_path}\n"

        if analysis_type == "cfg":
            message += f"    Basic blocks: {summary.get('basicBlocks', 'N/A')}\n"
        elif analysis_type == "call-graph":
            message += f"    Functions: {summary.get('functionCount', 'N/A')}\n"
            message += f"    Calls: {summary.get('callCount', 'N/A')}\n"
        elif analysis_type == "disassemble":
            message += f"    Instructions: {summary.get('instructionCount', 'N/A')}\n"
        elif analysis_type == "symbolic":
            message += f"    Paths analyzed: {summary.get('pathCount', 'N/A')}\n"

        message += f"    Output: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {
            "error": f"Thoth {analysis_type} timed out (10 minutes)",
            "outputFile": str(output_file)
        }
    except Exception as e:
        return {
            "error": f"Thoth execution error: {str(e)}",
            "outputFile": str(output_file)
        }


def parse_thoth_decompile(output: str) -> Dict:
    """Parse Thoth decompile output."""

    # Count functions in decompiled output
    function_count = len(re.findall(r'function\s+\w+', output, re.IGNORECASE))

    return {
        "functionCount": function_count
    }


def parse_thoth_analysis(output: str, analysis_type: str) -> Dict:
    """Parse Thoth analysis output based on type."""

    summary = {}

    if analysis_type == "cfg":
        # Count basic blocks
        basic_blocks = len(re.findall(r'Basic Block', output, re.IGNORECASE))
        summary["basicBlocks"] = basic_blocks

    elif analysis_type == "call-graph":
        # Count functions and calls
        functions = len(re.findall(r'Function:', output))
        calls = len(re.findall(r'calls', output, re.IGNORECASE))
        summary["functionCount"] = functions
        summary["callCount"] = calls

    elif analysis_type == "disassemble":
        # Count instructions
        instructions = len(re.findall(r'^\s*0x[0-9a-f]+:', output, re.MULTILINE))
        summary["instructionCount"] = instructions

    elif analysis_type == "symbolic":
        # Count paths
        paths = len(re.findall(r'Path\s+\d+', output))
        summary["pathCount"] = paths

    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Decompile remote: python thoth.py decompile --address <addr> --network <network> [engagement_dir]")
        print("  Decompile local:  python thoth.py decompile --path <path> [engagement_dir]")
        print("  Analyze remote:   python thoth.py analyze --address <addr> --network <network> --type <type> [engagement_dir]")
        print("  Analyze local:    python thoth.py analyze --path <path> --type <type> [engagement_dir]")
        print("")
        print("Analysis types: cfg, call-graph, disassemble, symbolic")
        print("")
        print("Examples:")
        print("  python thoth.py decompile --address 0x123... --network mainnet")
        print("  python thoth.py decompile --path compiled.json")
        print("  python thoth.py analyze --address 0x123... --network mainnet --type cfg")
        print("  python thoth.py analyze --path compiled.json --type call-graph")
        print("")
        print("Note: Repository no longer maintained but still functional")
        sys.exit(1)

    mode = sys.argv[1]

    # Simple argument parsing
    args = {}
    for i in range(2, len(sys.argv), 2):
        if i + 1 < len(sys.argv):
            key = sys.argv[i].lstrip('-')
            args[key] = sys.argv[i + 1]

    if mode == "decompile":
        result = thoth_decompile(
            contract_address=args.get('address', ''),
            network=args.get('network', 'mainnet'),
            contract_path=args.get('path', ''),
            engagement_dir=args.get('engagement', None)
        )

    elif mode == "analyze":
        result = thoth_analyze(
            contract_address=args.get('address', ''),
            network=args.get('network', 'mainnet'),
            contract_path=args.get('path', ''),
            analysis_type=args.get('type', 'cfg'),
            engagement_dir=args.get('engagement', None)
        )

    else:
        print(f"[!] Error: Unknown mode '{mode}'. Use 'decompile' or 'analyze'")
        sys.exit(1)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
