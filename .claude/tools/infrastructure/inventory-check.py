#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Infrastructure Inventory Checker

Purpose: Auto-generate infrastructure report from live systems
Usage: python tools/infrastructure/inventory-check.py
Output: docs/inventory-report-YYYYMMDD.md

This script connects to all infrastructure hosts and generates a
current state report to compare against the master inventory document.

Author: Claude Code + Chris Groves
Date: 2025-01-11
"""

import sys
import io
import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ASCII alternatives to emojis (Windows-safe)
CHECK = "[OK]"
CROSS = "[FAIL]"
WARNING = "[WARN]"
INFO = "[INFO]"
ARROW = "->"


class InfrastructureChecker:
    """Check live infrastructure and generate report"""

    def __init__(self):
        self.report = []
        self.claude_root = Path(os.path.expanduser("~/.claude"))
        if not self.claude_root.exists():
            self.claude_root = Path("C:/Users/Chris/.claude")

        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.report_file = self.claude_root / "docs" / f"inventory-report-{self.timestamp}.md"

    def log(self, message, level="INFO"):
        """Add message to report"""
        prefix = {
            "OK": CHECK,
            "FAIL": CROSS,
            "WARN": WARNING,
            "INFO": INFO
        }.get(level, INFO)

        line = f"{prefix} {message}"
        self.report.append(line)
        print(line)

    def check_local_system(self):
        """Check local Windows workstation"""
        self.log("=== HOST-001: Local Workstation ===", "INFO")

        # Check Claude Code root
        if self.claude_root.exists():
            self.log(f"Claude Code root exists: {self.claude_root}", "OK")
        else:
            self.log(f"Claude Code root NOT FOUND: {self.claude_root}", "FAIL")

        # Check Docker Desktop
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"Docker Desktop installed: {version}", "OK")

                # Check running containers
                result = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    containers = result.stdout.strip().split("\n")
                    container_count = len([c for c in containers if c])
                    self.log(f"Running containers: {container_count}", "INFO")

                    # Check for MCP Docker
                    mcp_containers = [c for c in containers if "mcp" in c.lower()]
                    if mcp_containers:
                        self.log(f"MCP Docker containers found: {len(mcp_containers)}", "OK")
                    else:
                        self.log("No MCP Docker containers found", "WARN")
            else:
                self.log("Docker Desktop installed but not running", "WARN")
        except FileNotFoundError:
            self.log("Docker Desktop NOT installed", "WARN")
        except subprocess.TimeoutExpired:
            self.log("Docker command timed out", "FAIL")
        except Exception as e:
            self.log(f"Docker check failed: {e}", "FAIL")

        # Check Twingate client
        # Note: No reliable CLI check for Twingate on Windows
        self.log("Twingate client check: Manual verification required", "INFO")

        # Check .mcp.json
        mcp_config = self.claude_root / ".mcp.json"
        if mcp_config.exists():
            self.log(".mcp.json exists", "OK")
            try:
                with open(mcp_config, 'r') as f:
                    config = json.load(f)
                    servers = config.get("mcpServers", {})
                    self.log(f"MCP servers configured: {len(servers)}", "INFO")
                    for name, details in servers.items():
                        url = details.get("url", "unknown")
                        self.log(f"  {ARROW} {name}: {url}", "INFO")
            except Exception as e:
                self.log(f".mcp.json parse failed: {e}", "FAIL")
        else:
            self.log(".mcp.json NOT FOUND", "FAIL")

    def check_remote_vps(self, hostname, ssh_user="root"):
        """Check remote VPS via SSH"""
        self.log(f"\n=== Checking {hostname} ===", "INFO")

        # Test SSH connectivity
        try:
            result = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                 f"{ssh_user}@{hostname}", "echo 'SSH OK'"],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0:
                self.log(f"SSH connectivity: OK", "OK")
            else:
                self.log(f"SSH connectivity: FAILED (check keys)", "FAIL")
                return  # Can't proceed without SSH
        except subprocess.TimeoutExpired:
            self.log(f"SSH connection timed out", "FAIL")
            return
        except Exception as e:
            self.log(f"SSH check failed: {e}", "FAIL")
            return

        # Get system info
        commands = {
            "OS": "cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'",
            "Uptime": "uptime -p",
            "RAM": "free -h | grep Mem | awk '{print $2 \" total, \" $3 \" used, \" $4 \" free\"}'",
            "Disk": "df -h / | tail -1 | awk '{print $2 \" total, \" $3 \" used, \" $4 \" free\"}'",
            "CPU": "nproc",
        }

        for label, cmd in commands.items():
            try:
                result = subprocess.run(
                    ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                     f"{ssh_user}@{hostname}", cmd],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                if result.returncode == 0:
                    output = result.stdout.strip()
                    self.log(f"{label}: {output}", "INFO")
                else:
                    self.log(f"{label}: Command failed", "FAIL")
            except Exception as e:
                self.log(f"{label}: Check failed - {e}", "FAIL")

        # Check Docker
        try:
            result = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                 f"{ssh_user}@{hostname}", "docker ps --format '{{.Names}}'"],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0:
                containers = result.stdout.strip().split("\n")
                container_count = len([c for c in containers if c])
                self.log(f"Docker containers running: {container_count}", "OK")
                if container_count > 0:
                    for container in containers:
                        if container:
                            self.log(f"  {ARROW} {container}", "INFO")
            else:
                self.log("Docker not installed or not running", "WARN")
        except Exception as e:
            self.log(f"Docker check failed: {e}", "FAIL")

    def check_external_services(self):
        """Check external services (Ghost, etc.)"""
        self.log("\n=== EXTERNAL-001: Ghost(Pro) Blog ===", "INFO")

        # Check Ghost blog availability
        try:
            import urllib.request
            import urllib.error

            url = "https://notchrisgroves.com"
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Infrastructure Check)')

            with urllib.request.urlopen(request, timeout=10) as response:
                status = response.status
                if status == 200:
                    self.log(f"Ghost blog reachable: {url}", "OK")
                else:
                    self.log(f"Ghost blog returned status: {status}", "WARN")
        except urllib.error.URLError as e:
            self.log(f"Ghost blog unreachable: {e}", "FAIL")
        except Exception as e:
            self.log(f"Ghost blog check failed: {e}", "FAIL")

    def generate_report(self):
        """Generate markdown report"""
        header = f"""# Infrastructure Inventory Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Tool:** tools/infrastructure/inventory-check.py
**Purpose:** Compare live infrastructure against master inventory

---

## Report

"""

        footer = f"""

---

## Next Steps

1. Compare this report to `docs/infrastructure-inventory.md`
2. Document any discrepancies
3. Update master inventory if changes are legitimate
4. Investigate unexpected changes (security concern)

**Report saved:** {self.report_file}
"""

        full_report = header + "\n".join(self.report) + footer

        # Save to file
        try:
            self.report_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write(full_report)
            print(f"\n{CHECK} Report saved: {self.report_file}")
        except Exception as e:
            print(f"\n{CROSS} Failed to save report: {e}")

    def run(self):
        """Run all checks"""
        print(f"{INFO} Starting infrastructure inventory check...")
        print(f"{INFO} Timestamp: {self.timestamp}\n")

        # Check local system
        self.check_local_system()

        # Check Hostinger VPS (if SSH configured)
        # NOTE: Replace with actual hostname when available
        # self.check_remote_vps("srv945980.hstgr.cloud", "root")
        self.log("\n=== HOST-002: Hostinger VPS ===", "INFO")
        self.log("Manual check required (SSH credentials not configured)", "WARN")

        # Check OVHcloud VPS (if deployed)
        # NOTE: Replace with actual hostname after deployment
        # self.check_remote_vps("ovh-vps-hostname", "root")
        self.log("\n=== HOST-003: OVHcloud VPS ===", "INFO")
        self.log("Not yet deployed (planned)", "INFO")

        # Check external services
        self.check_external_services()

        # Generate report
        self.generate_report()


def main():
    """Main entry point"""
    checker = InfrastructureChecker()
    checker.run()


if __name__ == "__main__":
    main()
