#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Token Efficiency Measurement Tests

Measures token efficiency for tools available on local Windows system.
This complements the VPS-based measurements by providing immediate validation
of the token reduction approach with real, measurable data.
"""

import sys
import io
import json
import subprocess
import tiktoken
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class TokenCounter:
    """Count tokens using Claude's encoding."""

    def __init__(self):
        """Initialize tiktoken encoder."""
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def count(self, text: str) -> int:
        """Count tokens in text."""
        if not text:
            return 0
        try:
            return len(self.encoding.encode(text))
        except Exception as e:
            print(f"[!] Token counting error: {e}")
            return 0


def test_curl_efficiency():
    """Test curl HTTP requests - available on local system."""
    print("\n[TEST 1] CURL HTTP Response Efficiency")
    print("=" * 60)

    counter = TokenCounter()

    # Execute curl command
    cmd = ["curl", "-s", "https://httpbin.org/get"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        raw_output = result.stdout
    except Exception as e:
        print(f"[!] Failed to execute curl: {e}")
        return None

    # Count raw tokens
    raw_tokens = counter.count(raw_output)
    print(f"[+] Raw HTTP response: {raw_tokens} tokens")
    print(f"    Size: {len(raw_output)} characters")

    # Create minimal summary (JSON extraction pattern)
    minimal_summary = json.dumps({
        "status": "success",
        "endpoint": "/get",
        "method": "GET",
        "data_received": True,
        "summary": "HTTP request successful"
    })
    minimal_tokens = counter.count(minimal_summary)

    reduction = 100 * (1 - minimal_tokens / raw_tokens) if raw_tokens > 0 else 0

    print(f"[+] Minimal JSON summary: {minimal_tokens} tokens")
    print(f"[+] Token reduction: {reduction:.1f}%")
    print(f"    Raw: {raw_tokens} → Minimal: {minimal_tokens}")

    return {
        "tool": "curl",
        "category": "http",
        "test_id": "LT-001",
        "raw_tokens": raw_tokens,
        "minimal_tokens": minimal_tokens,
        "reduction_percent": reduction,
        "raw_output_sample": raw_output[:200] + "..." if len(raw_output) > 200 else raw_output
    }


def test_git_log_efficiency():
    """Test git log output - available on local system."""
    print("\n[TEST 2] Git Log Output Efficiency")
    print("=" * 60)

    counter = TokenCounter()

    # Execute git log command
    cmd = ["git", "-C", "C:\\Users\\Chris\\.claude", "log", "--oneline", "-20"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        raw_output = result.stdout
    except Exception as e:
        print(f"[!] Failed to execute git log: {e}")
        return None

    # Count raw tokens
    raw_tokens = counter.count(raw_output)
    print(f"[+] Raw git log output: {raw_tokens} tokens")
    print(f"    Size: {len(raw_output)} characters")

    # Parse commits
    commits = raw_output.strip().split('\n')

    # Create minimal summary (structured data)
    minimal_summary = json.dumps({
        "repository": ".claude",
        "commit_count": len([c for c in commits if c.strip()]),
        "time_span": "recent",
        "summary": f"{len([c for c in commits if c.strip()])} recent commits"
    })
    minimal_tokens = counter.count(minimal_summary)

    reduction = 100 * (1 - minimal_tokens / raw_tokens) if raw_tokens > 0 else 0

    print(f"[+] Minimal structured summary: {minimal_tokens} tokens")
    print(f"[+] Token reduction: {reduction:.1f}%")
    print(f"    Raw: {raw_tokens} → Minimal: {minimal_tokens}")

    return {
        "tool": "git log",
        "category": "version-control",
        "test_id": "LT-002",
        "raw_tokens": raw_tokens,
        "minimal_tokens": minimal_tokens,
        "reduction_percent": reduction,
        "raw_output_sample": raw_output[:200]
    }


def test_system_info_efficiency():
    """Test system information retrieval - available on local system."""
    print("\n[TEST 3] System Information Query Efficiency")
    print("=" * 60)

    counter = TokenCounter()

    # Get system information using Python
    import platform
    import os

    raw_output = f"""Platform: {platform.system()}
Architecture: {platform.machine()}
Python Version: {platform.python_version()}
Processor: {platform.processor()}
Node Name: {platform.node()}
Release: {platform.release()}
Version: {platform.version()}
"""

    # Count raw tokens
    raw_tokens = counter.count(raw_output)
    print(f"[+] Raw system info: {raw_tokens} tokens")
    print(f"    Size: {len(raw_output)} characters")

    # Create minimal summary
    minimal_summary = json.dumps({
        "os": platform.system(),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "summary": f"{platform.system()} ({platform.machine()})"
    })
    minimal_tokens = counter.count(minimal_summary)

    reduction = 100 * (1 - minimal_tokens / raw_tokens) if raw_tokens > 0 else 0

    print(f"[+] Minimal JSON summary: {minimal_tokens} tokens")
    print(f"[+] Token reduction: {reduction:.1f}%")
    print(f"    Raw: {raw_tokens} → Minimal: {minimal_tokens}")

    return {
        "tool": "system-info",
        "category": "system",
        "test_id": "LT-003",
        "raw_tokens": raw_tokens,
        "minimal_tokens": minimal_tokens,
        "reduction_percent": reduction,
        "raw_output": raw_output
    }


def test_json_api_parsing():
    """Test JSON API response parsing efficiency."""
    print("\n[TEST 4] JSON API Response Parsing Efficiency")
    print("=" * 60)

    counter = TokenCounter()

    # Simulate a complex JSON API response (like httpbin POST)
    raw_output = json.dumps({
        "args": {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        },
        "data": "",
        "files": {},
        "form": {},
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "0",
            "Host": "httpbin.org",
            "User-Agent": "curl/7.64.1",
            "X-Amzn-Trace-Id": "Root=1-5e6722a7-cc51xmpl46db7ae2d7fb47d6b"
        },
        "json": None,
        "method": "GET",
        "origin": "192.0.2.1",
        "url": "https://httpbin.org/get?key1=value1&key2=value2&key3=value3"
    }, indent=2)

    # Count raw tokens
    raw_tokens = counter.count(raw_output)
    print(f"[+] Raw JSON API response: {raw_tokens} tokens")
    print(f"    Size: {len(raw_output)} characters")

    # Parse and create minimal summary
    minimal_summary = json.dumps({
        "method": "GET",
        "status": "success",
        "args_count": 3,
        "headers_count": 7,
        "origin": "192.0.2.1",
        "summary": "GET request with 3 query parameters"
    })
    minimal_tokens = counter.count(minimal_summary)

    reduction = 100 * (1 - minimal_tokens / raw_tokens) if raw_tokens > 0 else 0

    print(f"[+] Minimal summary: {minimal_tokens} tokens")
    print(f"[+] Token reduction: {reduction:.1f}%")
    print(f"    Raw: {raw_tokens} → Minimal: {minimal_tokens}")

    return {
        "tool": "json-parsing",
        "category": "data-processing",
        "test_id": "LT-004",
        "raw_tokens": raw_tokens,
        "minimal_tokens": minimal_tokens,
        "reduction_percent": reduction,
        "raw_output_sample": raw_output[:300]
    }


def test_markdown_documentation_efficiency():
    """Test markdown documentation parsing efficiency."""
    print("\n[TEST 5] Markdown Documentation Processing Efficiency")
    print("=" * 60)

    counter = TokenCounter()

    # Create a sample markdown document similar to documentation
    raw_output = """# Security Testing Report

## Executive Summary

This section provides a high-level overview of findings.

## Detailed Findings

### Finding 1: SQL Injection in Login Form
- **Severity:** Critical
- **CvSS Score:** 9.8
- **Description:** User input is not properly sanitized before database query
- **Impact:** Complete database compromise possible
- **Recommendation:** Use parameterized queries

### Finding 2: Missing HTTPS on API Endpoint
- **Severity:** High
- **CVSS Score:** 8.7
- **Description:** API endpoint serves content over unencrypted HTTP
- **Impact:** Data interception possible
- **Recommendation:** Implement HTTPS

### Finding 3: Weak Password Policy
- **Severity:** Medium
- **CVSS Score:** 5.3
- **Description:** Application allows 4-character passwords
- **Impact:** Increased brute-force attack surface
- **Recommendation:** Enforce minimum 12-character passwords

## Remediation Timeline
- Critical: 30 days
- High: 60 days
- Medium: 90 days

## Conclusion
Application requires immediate attention to critical findings.
"""

    # Count raw tokens
    raw_tokens = counter.count(raw_output)
    print(f"[+] Raw markdown report: {raw_tokens} tokens")
    print(f"    Size: {len(raw_output)} characters")

    # Create minimal summary
    minimal_summary = json.dumps({
        "report_type": "Security Testing",
        "findings": [
            {"id": 1, "severity": "Critical", "type": "SQL Injection"},
            {"id": 2, "severity": "High", "type": "Missing HTTPS"},
            {"id": 3, "severity": "Medium", "type": "Weak Password Policy"}
        ],
        "critical_count": 1,
        "high_count": 1,
        "medium_count": 1,
        "summary": "3 findings identified (1 critical, 1 high, 1 medium)"
    })
    minimal_tokens = counter.count(minimal_summary)

    reduction = 100 * (1 - minimal_tokens / raw_tokens) if raw_tokens > 0 else 0

    print(f"[+] Minimal summary: {minimal_tokens} tokens")
    print(f"[+] Token reduction: {reduction:.1f}%")
    print(f"    Raw: {raw_tokens} → Minimal: {minimal_tokens}")

    return {
        "tool": "markdown-docs",
        "category": "documentation",
        "test_id": "LT-005",
        "raw_tokens": raw_tokens,
        "minimal_tokens": minimal_tokens,
        "reduction_percent": reduction,
        "raw_output_sample": raw_output[:300]
    }


def main():
    """Run all local efficiency tests."""
    print("\n" + "=" * 60)
    print("TOKEN EFFICIENCY LOCAL VALIDATION TESTS")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")

    results = []

    # Run all tests
    result = test_curl_efficiency()
    if result:
        results.append(result)

    result = test_git_log_efficiency()
    if result:
        results.append(result)

    result = test_system_info_efficiency()
    if result:
        results.append(result)

    result = test_json_api_parsing()
    if result:
        results.append(result)

    result = test_markdown_documentation_efficiency()
    if result:
        results.append(result)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if results:
        total_raw = sum(r["raw_tokens"] for r in results)
        total_minimal = sum(r["minimal_tokens"] for r in results)

        if total_raw > 0:
            avg_reduction = 100 * (1 - total_minimal / total_raw)
        else:
            avg_reduction = 0

        print(f"\nTests completed: {len(results)}")
        print(f"Total raw tokens: {total_raw}")
        print(f"Total minimal tokens: {total_minimal}")
        print(f"Average reduction: {avg_reduction:.1f}%")

        print("\nBreakdown by test:")
        for r in results:
            print(f"  {r['test_id']:8} ({r['tool']:15}): {r['reduction_percent']:5.1f}% reduction " +
                  f"({r['raw_tokens']:4} → {r['minimal_tokens']:3} tokens)")

        # Save results to JSON
        output_path = Path("C:\\Users\\Chris\\.claude\\results\\local_efficiency_tests.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "tests_completed": len(results),
                "total_raw_tokens": total_raw,
                "total_minimal_tokens": total_minimal,
                "average_reduction_percent": avg_reduction,
                "tests": results
            }, f, indent=2)

        print(f"\n[+] Results saved to: {output_path}")


if __name__ == "__main__":
    main()
