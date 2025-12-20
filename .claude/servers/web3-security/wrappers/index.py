#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web3 Security MCP Server - Code API Pattern
Tool registry and exploration interface
"""

# Tool Registry
TOOLS = {
    "static_analysis": {
        "slither": {
            "description": "Solidity static analyzer - detects vulnerabilities in smart contracts",
            "module": "slither",
            "function": "slither",
            "params": {
                "contract_path": "Path to Solidity file or GitHub repo URL",
                "detectors": "Optional specific detectors to run",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Vulnerability summary by severity"
        },
        "mythril": {
            "description": "Security analysis tool using symbolic execution",
            "module": "mythril",
            "function": "mythril",
            "params": {
                "contract_path": "Path to Solidity file",
                "contract_address": "Optional deployed contract address",
                "rpc_url": "Optional RPC URL for deployed contracts",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Security issues with severity and locations"
        },
        "semgrep": {
            "description": "Pattern-based static analysis for smart contracts",
            "module": "semgrep",
            "function": "semgrep",
            "params": {
                "contract_path": "Path to contract directory or file",
                "rules": "Ruleset to use (default: p/smart-contracts)",
                "output_format": "Output format: text, json, sarif",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Vulnerability findings by severity"
        }
    },
    "fuzzing_verification": {
        "echidna": {
            "description": "Property-based fuzzing for Solidity contracts",
            "module": "echidna",
            "function": "echidna",
            "params": {
                "contract_path": "Path to Solidity contract",
                "config_file": "Optional echidna.yaml config path",
                "timeout": "Max fuzzing time in seconds (default: 300)",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Property violations and counterexamples"
        },
        "halmos": {
            "description": "Formal verification using symbolic execution",
            "module": "halmos",
            "function": "halmos",
            "params": {
                "contract_path": "Path to contract or project directory",
                "function_name": "Optional specific function to verify",
                "solver_timeout": "Max solver time per assertion (default: 300)",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Verification results and assertion violations"
        }
    },
    "testing": {
        "forge_test": {
            "description": "Run Foundry test suite with gas reporting",
            "module": "forge",
            "function": "forge_test",
            "params": {
                "project_path": "Path to Foundry project directory",
                "match_test": "Optional pattern to match test names",
                "gas_report": "Enable gas reporting (true/false)",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Test results and gas usage"
        },
        "forge_coverage": {
            "description": "Generate code coverage report",
            "module": "forge",
            "function": "forge_coverage",
            "params": {
                "project_path": "Path to Foundry project directory",
                "report_file": "Optional output file for LCOV report",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Coverage metrics and uncovered paths"
        }
    },
    "blockchain_interaction": {
        "cast_call": {
            "description": "Execute read-only contract function calls",
            "module": "cast",
            "function": "cast_call",
            "params": {
                "contract_address": "Contract address to call",
                "function_signature": "Function signature (e.g., 'balanceOf(address)')",
                "rpc_url": "RPC endpoint URL",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Function call results"
        },
        "cast_storage": {
            "description": "Read contract storage slot values",
            "module": "cast",
            "function": "cast_storage",
            "params": {
                "contract_address": "Contract address",
                "storage_slot": "Storage slot number",
                "rpc_url": "RPC endpoint URL",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Storage slot value"
        },
        "cast_abi_decode": {
            "description": "Decode ABI-encoded data",
            "module": "cast",
            "function": "cast_abi_decode",
            "params": {
                "data_type": "Data type signature",
                "calldata": "Hex-encoded data to decode",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "direct",
            "returns": "Decoded data"
        },
        "cast_4byte": {
            "description": "Get function signature from 4byte selector",
            "module": "cast",
            "function": "cast_4byte",
            "params": {
                "signature": "4byte function selector",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "direct",
            "returns": "Function signature(s)"
        },
        "cast_4byte_decode": {
            "description": "Decode calldata using 4byte directory",
            "module": "cast",
            "function": "cast_4byte_decode",
            "params": {
                "calldata": "Transaction calldata to decode",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "direct",
            "returns": "Decoded function call"
        }
    },
    "compiler_management": {
        "solc_versions": {
            "description": "List available and installed Solidity compiler versions",
            "module": "solc",
            "function": "solc_versions",
            "output": "direct",
            "returns": "List of compiler versions"
        },
        "solc_install": {
            "description": "Install specific Solidity compiler version",
            "module": "solc",
            "function": "solc_install",
            "params": {
                "version": "Solidity version to install (e.g., 0.8.19)"
            },
            "output": "direct",
            "returns": "Installation status"
        },
        "solc_use": {
            "description": "Switch to specific Solidity compiler version",
            "module": "solc",
            "function": "solc_use",
            "params": {
                "version": "Solidity version to activate"
            },
            "output": "direct",
            "returns": "Activation status"
        }
    },
    "development": {
        "brownie_compile": {
            "description": "Compile smart contract project using Brownie",
            "module": "brownie",
            "function": "brownie_compile",
            "params": {
                "project_path": "Path to Brownie project directory",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Compilation results and artifacts"
        }
    },
    "cairo_static_analysis": {
        "caracal_detect": {
            "description": "Static analyzer for Cairo/Starknet contracts (SIERRA representation)",
            "module": "caracal",
            "function": "caracal_detect",
            "params": {
                "contract_path": "Path to Cairo contract file or project directory",
                "detectors": "Optional specific detectors to run",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Vulnerability summary by severity (Cairo/Starknet)"
        },
        "caracal_print": {
            "description": "Generate Caracal visualizations (CFG, call graphs)",
            "module": "caracal",
            "function": "caracal_print",
            "params": {
                "contract_path": "Path to Cairo contract file or project directory",
                "printer": "Type of output: cfg, call-graph, function-summary",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Visualization files and .dot graphs"
        },
        "amarna_lint": {
            "description": "Static analysis and linting for Cairo contracts (SARIF output)",
            "module": "amarna",
            "function": "amarna_lint",
            "params": {
                "contract_path": "Path to Cairo contract file or project directory",
                "rules": "Optional specific rules to enable",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Linting issues in SARIF format"
        }
    },
    "cairo_bytecode_analysis": {
        "thoth_decompile": {
            "description": "Decompile Cairo bytecode to readable format",
            "module": "thoth",
            "function": "thoth_decompile",
            "params": {
                "contract_address": "Optional deployed contract address (for remote analysis)",
                "network": "Starknet network: mainnet, goerli, sepolia (default: mainnet)",
                "contract_path": "Optional path to local compiled contract JSON",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Decompiled Cairo contract code"
        },
        "thoth_analyze": {
            "description": "Analyze Cairo bytecode structure and control flow",
            "module": "thoth",
            "function": "thoth_analyze",
            "params": {
                "contract_address": "Optional deployed contract address (for remote analysis)",
                "network": "Starknet network: mainnet, goerli, sepolia (default: mainnet)",
                "contract_path": "Optional path to local compiled contract JSON",
                "analysis_type": "Type: cfg, call-graph, disassemble, symbolic (default: cfg)",
                "engagement_dir": "Optional engagement directory path"
            },
            "output": "file",
            "returns": "Bytecode analysis results (CFG, call graph, etc.)"
        }
    }
}


def list_tools(category: str = None, detail_level: str = "summary") -> dict:
    """
    List available tools with optional filtering.

    Args:
        category: Filter by category (static_analysis, fuzzing_verification, etc.)
        detail_level: "summary" (names only), "descriptions", or "full" (all details)

    Returns:
        Dict of tools organized by category
    """

    if category and category in TOOLS:
        tools = {category: TOOLS[category]}
    else:
        tools = TOOLS

    if detail_level == "summary":
        # Return tool names only
        return {
            cat: list(tools_dict.keys())
            for cat, tools_dict in tools.items()
        }
    elif detail_level == "descriptions":
        # Return names + descriptions
        return {
            cat: {
                name: tool["description"]
                for name, tool in tools_dict.items()
            }
            for cat, tools_dict in tools.items()
        }
    else:  # full
        return tools


def search_tools(keyword: str) -> dict:
    """
    Search tools by keyword in name or description.

    Args:
        keyword: Search term

    Returns:
        Dict of matching tools
    """

    matches = {}
    keyword_lower = keyword.lower()

    for category, tools_dict in TOOLS.items():
        for name, tool in tools_dict.items():
            if (keyword_lower in name.lower() or
                keyword_lower in tool["description"].lower()):
                if category not in matches:
                    matches[category] = {}
                matches[category][name] = tool

    return matches


if __name__ == "__main__":
    import json

    print("=== Web3 Security Tool Registry ===\n")

    print("Tool Summary:")
    print(json.dumps(list_tools(detail_level="summary"), indent=2))

    print("\n\nSearch 'fuzzing':")
    print(json.dumps(search_tools("fuzzing"), indent=2))
