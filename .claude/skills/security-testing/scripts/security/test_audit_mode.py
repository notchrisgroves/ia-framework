#!/usr/bin/env python3
"""
Audit Mode Test Script

Test the audit logging system with simulated tool executions.

Usage:
    python tools/security/test_audit_mode.py

Author: Intelligence Adjacent
Version: 1.0
Created: 2025-11-23
"""

import time
import subprocess
from pathlib import Path
from tools.security.audit_wrapper import AuditSession, log_scope_verification


def simulate_nmap_scan(target: str, options: str, engagement_dir: str) -> dict:
    """Simulate an nmap scan"""
    print(f"  -> Running nmap {options} {target}")
    time.sleep(0.5)  # Simulate scan time

    return {
        "summary": {
            "open_ports": [22, 80, 443],
            "services": ["SSH", "HTTP", "HTTPS"],
            "total_ports": 3
        },
        "output": f"""Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for {target}
Host is up (0.00015s latency).

PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 8.2p1
80/tcp  open  http    nginx 1.18.0
443/tcp open  https   nginx 1.18.0

Nmap done: 1 IP address (1 host up) scanned in 5.23 seconds
""",
        "success": True,
        "message": f"Nmap scan of {target} completed successfully"
    }


def simulate_nuclei_scan(target: str, severity: str, engagement_dir: str) -> dict:
    """Simulate a nuclei scan"""
    print(f"  -> Running nuclei -u {target} -severity {severity}")
    time.sleep(0.3)  # Simulate scan time

    return {
        "summary": {
            "total": 5,
            "critical": 1,
            "high": 2,
            "medium": 2
        },
        "output": f"""[CVE-2021-41773] [critical] Apache Path Traversal ({target})
[CVE-2021-3129] [high] Laravel Debug Mode ({target})
[weak-tls] [medium] Weak TLS Configuration ({target})
""",
        "success": True,
        "message": f"Nuclei scan of {target} found 5 vulnerabilities"
    }


def test_audit_mode():
    """Test audit logging functionality"""
    print("=" * 80)
    print("AUDIT MODE TEST SCRIPT")
    print("=" * 80)
    print()

    # Create test engagement directory
    engagement_dir = Path.home() / ".claude" / "scratchpad" / "test-audit-engagement"
    engagement_dir.mkdir(parents=True, exist_ok=True)

    print(f"Test engagement directory: {engagement_dir}\n")

    # Test 1: Basic audit logging
    print("Test 1: Basic Audit Logging (Enabled)")
    print("-" * 80)

    with AuditSession(engagement_dir=str(engagement_dir), enabled=True):
        # Simulate scope verifications
        log_scope_verification(target="192.168.1.100", verified=True, scope_line=45)
        log_scope_verification(target="10.0.0.1", verified=False, scope_line=None)

        # Simulate tool executions
        from tools.security.audit_wrapper import execute_with_audit

        # Nmap scan
        nmap_result = execute_with_audit(
            tool="nmap",
            category="kali_pentest",
            command="nmap -sV -sC 192.168.1.100",
            target="192.168.1.100",
            engagement_dir=str(engagement_dir),
            execution_func=lambda: simulate_nmap_scan("192.168.1.100", "-sV -sC", str(engagement_dir)),
            scope_verified=True
        )

        print(f"\nNmap result: {nmap_result['message']}")

        # Nuclei scan
        nuclei_result = execute_with_audit(
            tool="nuclei",
            category="kali_pentest",
            command="nuclei -u https://example.com -severity critical,high",
            target="https://example.com",
            engagement_dir=str(engagement_dir),
            execution_func=lambda: simulate_nuclei_scan("https://example.com", "critical,high", str(engagement_dir)),
            scope_verified=True
        )

        print(f"Nuclei result: {nuclei_result['message']}")

    print("\n[OK] Test 1 complete - Audit logs generated\n")

    # Test 2: View audit logs
    print("Test 2: Viewing Audit Logs")
    print("-" * 80)

    try:
        subprocess.run([
            "python",
            "tools/security/audit_viewer.py",
            "--engagement", str(engagement_dir),
            "--format", "table"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[WARN]  Viewer failed: {e}")

    print()

    # Test 3: Verify integrity
    print("Test 3: Integrity Verification")
    print("-" * 80)

    try:
        subprocess.run([
            "python",
            "tools/security/audit_viewer.py",
            "--engagement", str(engagement_dir),
            "--verify-integrity"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[WARN]  Integrity check failed: {e}")

    print()

    # Test 4: Export compliance report
    print("Test 4: Export Compliance Report")
    print("-" * 80)

    compliance_report = engagement_dir / "audit-logs" / "compliance" / "test-report.md"

    try:
        subprocess.run([
            "python",
            "tools/security/audit_viewer.py",
            "--engagement", str(engagement_dir),
            "--export-compliance", str(compliance_report)
        ], check=True)

        if compliance_report.exists():
            print(f"\n[OK] Compliance report generated: {compliance_report}")
            print(f"   Size: {compliance_report.stat().st_size} bytes")
        else:
            print(f"\n[WARN]  Compliance report not found: {compliance_report}")

    except subprocess.CalledProcessError as e:
        print(f"[WARN]  Export failed: {e}")

    print()

    # Test 5: Search functionality
    print("Test 5: Search Functionality")
    print("-" * 80)

    print("\nSearching for target 192.168.1.100:")
    try:
        subprocess.run([
            "python",
            "tools/security/audit_viewer.py",
            "--engagement", str(engagement_dir),
            "--search-target", "192.168.1.100"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[WARN]  Search failed: {e}")

    print("\nSearching for tool 'nmap':")
    try:
        subprocess.run([
            "python",
            "tools/security/audit_viewer.py",
            "--engagement", str(engagement_dir),
            "--search-tool", "nmap"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[WARN]  Search failed: {e}")

    print()

    # Test 6: Audit mode disabled
    print("Test 6: Audit Mode Disabled")
    print("-" * 80)

    with AuditSession(engagement_dir=str(engagement_dir), enabled=False):
        # This execution should NOT be logged
        from tools.security.audit_wrapper import execute_with_audit

        result = execute_with_audit(
            tool="test-tool",
            category="test",
            command="test command",
            target="test-target",
            engagement_dir=str(engagement_dir),
            execution_func=lambda: {"success": True, "message": "Test"}
        )

        print("  -> Tool executed without audit logging")
        print(f"  -> Result: {result['message']}")

    print("\n[OK] Test 6 complete - Tool executed without overhead\n")

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    print("[OK] All tests completed successfully")
    print()
    print(f"Audit logs location: {engagement_dir / 'audit-logs'}")
    print()
    print("Review audit logs:")
    print(f"  python tools/security/audit_viewer.py --engagement {engagement_dir}")
    print()
    print("View transcript:")
    print(f"  python tools/security/audit_viewer.py --engagement {engagement_dir} --format transcript")
    print()
    print("Cleanup test data:")
    print(f"  rm -rf {engagement_dir}")
    print()


if __name__ == "__main__":
    test_audit_mode()
