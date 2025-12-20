#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mobile Security tool registry and search"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

TOOLS = {
    "apktool": {
        "name": "apktool",
        "description": "APK decompilation - Extract resources and smali code",
        "category": "decompilation",
        "function": "apktool_decode"
    },
    "jadx": {
        "name": "jadx",
        "description": "Java decompiler - Convert APK to readable Java source",
        "category": "decompilation",
        "function": "jadx_decompile"
    },
    "androguard": {
        "name": "androguard",
        "description": "Static analysis - Permissions, activities, services, security issues",
        "category": "static-analysis",
        "function": "androguard_analyze"
    },
    "apksigner": {
        "name": "apksigner",
        "description": "Signature verification - Certificate and signing info",
        "category": "verification",
        "function": "apksigner_verify"
    },
    "aapt": {
        "name": "aapt",
        "description": "APK metadata extraction - Manifest, permissions, package info",
        "category": "metadata",
        "function": "aapt_dump"
    },
    "apkleaks": {
        "name": "apkleaks",
        "description": "Hardcoded secrets scanner - API keys, URLs, credentials",
        "category": "secret-scanning",
        "function": "apkleaks_scan"
    },
    "frida": {
        "name": "frida",
        "description": "Dynamic instrumentation - List running processes",
        "category": "dynamic",
        "function": "frida_ps"
    },
    "objection": {
        "name": "objection",
        "description": "Mobile app security testing - Runtime exploration",
        "category": "dynamic",
        "function": "objection_explore"
    }
}

def list_tools(detail_level: str = "names") -> dict:
    """
    List mobile security tools.

    Args:
        detail_level: "names" (just names), "descriptions" (with descriptions), "full" (all metadata)

    Returns:
        Dict with tool information
    """
    if detail_level == "names":
        return {"tools": list(TOOLS.keys()), "count": len(TOOLS)}
    elif detail_level == "descriptions":
        return {
            "tools": {name: tool["description"] for name, tool in TOOLS.items()},
            "count": len(TOOLS)
        }
    else:  # full
        return {"tools": TOOLS, "count": len(TOOLS)}

def search_tools(query: str) -> dict:
    """
    Search tools by name or description.

    Args:
        query: Search term

    Returns:
        Dict with matching tools
    """
    query_lower = query.lower()
    matches = {
        name: tool for name, tool in TOOLS.items()
        if query_lower in name.lower() or query_lower in tool["description"].lower()
    }
    return {"matches": matches, "count": len(matches)}

if __name__ == "__main__":
    import json
    print(json.dumps(list_tools("descriptions"), indent=2))
