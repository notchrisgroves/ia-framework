#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token Efficiency Measurement Script

Measures actual token reduction for VPS Code API wrapper pattern
using tiktoken (Claude's token counter).

Usage:
    python measure_efficiency.py --run-all              # Run all tests
    python measure_efficiency.py --tool nmap            # Run specific tool tests
    python measure_efficiency.py --category pentest     # Run category tests
    python measure_efficiency.py --analyze results.json # Analyze results
"""

import sys
import io
import json
import subprocess
import tiktoken
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


@dataclass
class TokenMeasurement:
    """Single measurement of token usage."""
    tool: str
    category: str
    test_id: str
    test_target: str
    command: str

    # Output data
    raw_output: str
    raw_tokens: int

    # Minimal mode summary
    minimal_summary: str
    minimal_tokens: int

    # Standard mode summary
    standard_summary: Optional[str] = None
    standard_tokens: Optional[int] = None

    # Metadata
    timestamp: str = None
    duration_seconds: float = 0.0
    error: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    @property
    def minimal_reduction(self) -> float:
        """Percentage reduction in minimal mode."""
        if self.raw_tokens == 0:
            return 0
        return 100 * (1 - self.minimal_tokens / self.raw_tokens)

    @property
    def standard_reduction(self) -> Optional[float]:
        """Percentage reduction in standard mode."""
        if not self.standard_tokens or self.raw_tokens == 0:
            return None
        return 100 * (1 - self.standard_tokens / self.raw_tokens)


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


class ToolExecutor:
    """Execute tools and capture output."""

    def __init__(self, use_vps: bool = False):
        """
        Initialize executor.

        Args:
            use_vps: Whether to execute on VPS via SSH (requires Twingate)
        """
        self.use_vps = use_vps
        self.ssh_host = "debian@15.204.218.153"
        self.ssh_port = 2222

    def run_local(self, command: str, timeout: int = 60) -> Tuple[str, int, str]:
        """
        Run command locally.

        Returns:
            (stdout, return_code, stderr)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout, result.returncode, result.stderr
        except subprocess.TimeoutExpired:
            return "", 1, "Command timeout"
        except Exception as e:
            return "", 1, str(e)

    def run_vps(self, command: str, timeout: int = 300) -> Tuple[str, int, str]:
        """
        Run command on VPS via SSH.

        Returns:
            (stdout, return_code, stderr)
        """
        if not self.use_vps:
            return self.run_local(command, timeout)

        ssh_cmd = f"ssh -p {self.ssh_port} {self.ssh_host} '{command}'"
        return self.run_local(ssh_cmd, timeout)


class TestHarness:
    """Run efficiency tests for VPS tools."""

    # Test definitions
    PENTEST_TESTS = {
        "PT-001": {
            "tool": "nmap",
            "target": "scanme.nmap.org",
            "command": "nmap -sV -sC -p- --top-ports 100 scanme.nmap.org",
            "timeout": 120,
            "expected_raw_tokens": (2500, 3500),
        },
        "PT-002": {
            "tool": "nuclei",
            "target": "httpbin.org",
            "command": "echo 'https://httpbin.org' | nuclei -t /root/.nuclei-templates/http/default-logins.yaml -silent 2>/dev/null || echo '[no vulnerabilities found]'",
            "timeout": 60,
            "expected_raw_tokens": (500, 1500),  # Reduced expectation for safe target
        },
        "PT-003": {
            "tool": "httpx",
            "target": "httpbin.org",
            "command": "echo 'httpbin.org' | httpx -status -title -tech -silent",
            "timeout": 30,
            "expected_raw_tokens": (200, 800),
        },
        "PT-004": {
            "tool": "whois",
            "target": "example.com",
            "command": "whois example.com 2>/dev/null | head -50",
            "timeout": 10,
            "expected_raw_tokens": (200, 600),
        },
        "PT-005": {
            "tool": "curl",
            "target": "httpbin.org",
            "command": "curl -s https://httpbin.org/get | head -100",
            "timeout": 10,
            "expected_raw_tokens": (200, 800),
        },
    }

    def __init__(self, use_vps: bool = False, output_dir: Optional[str] = None):
        """Initialize test harness."""
        self.counter = TokenCounter()
        self.executor = ToolExecutor(use_vps=use_vps)
        self.use_vps = use_vps

        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "token-measurements"

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.measurements: List[TokenMeasurement] = []

    def run_test(self, test_id: str, category: str, test_config: Dict) -> TokenMeasurement:
        """Run single efficiency test."""
        print(f"\n[*] Running {test_id} ({test_config['tool']})...")

        start_time = datetime.now()

        # Execute tool
        stdout, returncode, stderr = self.executor.run_vps(
            test_config['command'],
            timeout=test_config['timeout']
        )

        if returncode != 0:
            print(f"[!] Test failed: {stderr}")
            measurement = TokenMeasurement(
                tool=test_config['tool'],
                category=category,
                test_id=test_id,
                test_target=test_config['target'],
                command=test_config['command'],
                raw_output="",
                raw_tokens=0,
                minimal_summary="",
                minimal_tokens=0,
                error=stderr[:200]
            )
            return measurement

        # Count raw output tokens
        raw_tokens = self.counter.count(stdout)
        print(f"    Raw output: {raw_tokens} tokens")

        # Create minimal summary (example implementation)
        minimal_summary = self._create_minimal_summary(test_config['tool'], stdout)
        minimal_tokens = self.counter.count(minimal_summary)
        print(f"    Minimal summary: {minimal_tokens} tokens")

        # Create standard summary
        standard_summary = self._create_standard_summary(test_config['tool'], stdout)
        standard_tokens = self.counter.count(standard_summary) if standard_summary else None
        if standard_tokens:
            print(f"    Standard summary: {standard_tokens} tokens")

        # Calculate reduction
        minimal_reduction = 100 * (1 - minimal_tokens / raw_tokens) if raw_tokens > 0 else 0
        print(f"    Minimal reduction: {minimal_reduction:.1f}%")

        duration = (datetime.now() - start_time).total_seconds()

        measurement = TokenMeasurement(
            tool=test_config['tool'],
            category=category,
            test_id=test_id,
            test_target=test_config['target'],
            command=test_config['command'],
            raw_output=stdout[:500],  # Store first 500 chars for reference
            raw_tokens=raw_tokens,
            minimal_summary=minimal_summary[:200],  # Store first 200 chars
            minimal_tokens=minimal_tokens,
            standard_summary=standard_summary[:200] if standard_summary else None,
            standard_tokens=standard_tokens,
            duration_seconds=duration
        )

        self.measurements.append(measurement)
        return measurement

    def _create_minimal_summary(self, tool: str, output: str) -> str:
        """Create minimal summary for tool output."""
        lines = output.split('\n')

        if tool == "nmap":
            # Extract open ports
            open_ports = []
            for line in lines:
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    if parts:
                        open_ports.append(parts[0].split('/')[0])

            return json.dumps({
                "tool": "nmap",
                "openPorts": open_ports[:10],
                "portCount": len(open_ports),
                "summary": f"Found {len(open_ports)} open ports"
            })

        elif tool == "nuclei":
            # Count findings
            findings = [l for l in lines if '[' in l and ']' in l]
            return json.dumps({
                "tool": "nuclei",
                "findingCount": len(findings),
                "summary": f"Found {len(findings)} potential vulnerabilities"
            })

        elif tool == "httpx":
            # Extract status codes
            status_codes = []
            for line in lines:
                if '[' in line and ']' in line:
                    status_codes.append(line.strip())

            return json.dumps({
                "tool": "httpx",
                "responseCount": len(status_codes),
                "topResponses": status_codes[:3],
                "summary": f"Probed {len(status_codes)} endpoints"
            })

        elif tool == "whois":
            # Extract key information
            registrant_line = next((l for l in lines if 'Registrant' in l), None)
            return json.dumps({
                "tool": "whois",
                "lines": len(lines),
                "hasRegistrant": registrant_line is not None,
                "summary": f"WHOIS record ({len(lines)} lines)"
            })

        elif tool == "curl":
            # Extract HTTP response
            status_line = next((l for l in lines if '"' in l), None)
            return json.dumps({
                "tool": "curl",
                "lines": len(lines),
                "summary": "HTTP response retrieved"
            })

        else:
            # Generic summary
            return json.dumps({
                "tool": tool,
                "lines": len([l for l in lines if l.strip()]),
                "summary": "Tool executed successfully"
            })

    def _create_standard_summary(self, tool: str, output: str) -> Optional[str]:
        """Create standard summary for tool output."""
        lines = output.split('\n')
        summary_lines = []

        # Include more details than minimal
        if tool == "nmap":
            summary_lines = lines[:50]  # First 50 lines
        elif tool in ["nuclei", "httpx"]:
            summary_lines = lines[:30]
        elif tool == "whois":
            summary_lines = lines[:40]
        else:
            summary_lines = lines[:20]

        return "\n".join(summary_lines) if summary_lines else None

    def run_all_pentest_tests(self) -> List[TokenMeasurement]:
        """Run all pentest tests."""
        print("\n=== PENTEST TOOLS TESTS ===")
        results = []
        for test_id, config in self.PENTEST_TESTS.items():
            result = self.run_test(test_id, "pentest", config)
            results.append(result)
        return results

    def save_results(self, filename: str = "token_measurements.json"):
        """Save measurements to JSON file."""
        output_file = self.output_dir / filename

        measurements_dict = [asdict(m) for m in self.measurements]

        with open(output_file, 'w') as f:
            json.dump(measurements_dict, f, indent=2)

        print(f"\n[+] Results saved to {output_file}")
        return output_file

    def print_summary(self):
        """Print summary of all measurements."""
        print("\n=== TOKEN EFFICIENCY SUMMARY ===\n")

        if not self.measurements:
            print("No measurements recorded")
            return

        # Summary statistics
        total_raw = sum(m.raw_tokens for m in self.measurements if m.error is None)
        total_minimal = sum(m.minimal_tokens for m in self.measurements if m.error is None)

        if total_raw > 0:
            average_reduction = 100 * (1 - total_minimal / total_raw)
        else:
            average_reduction = 0

        print(f"Tests run: {len(self.measurements)}")
        print(f"Successful: {len([m for m in self.measurements if m.error is None])}")
        print(f"Failed: {len([m for m in self.measurements if m.error is not None])}\n")

        print(f"Total raw tokens: {total_raw}")
        print(f"Total minimal tokens: {total_minimal}")
        print(f"Average reduction: {average_reduction:.1f}%\n")

        # Per-tool breakdown
        print("Per-tool measurements:")
        print("-" * 80)
        print(f"{'Tool':<20} {'Category':<15} {'Raw':<10} {'Min':<10} {'Reduction':<12}")
        print("-" * 80)

        for m in self.measurements:
            if m.error is None:
                reduction = f"{m.minimal_reduction:.1f}%"
            else:
                reduction = f"ERROR"

            print(f"{m.tool:<20} {m.category:<15} {m.raw_tokens:<10} {m.minimal_tokens:<10} {reduction:<12}")

        print("-" * 80)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Measure token efficiency of VPS Code API wrapper pattern"
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all tests"
    )
    parser.add_argument(
        "--category",
        choices=["pentest", "web3", "mobile", "research", "database"],
        help="Run tests for specific category"
    )
    parser.add_argument(
        "--tool",
        help="Run tests for specific tool"
    )
    parser.add_argument(
        "--vps",
        action="store_true",
        help="Execute tests on VPS (requires Twingate)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for results"
    )
    parser.add_argument(
        "--analyze",
        help="Analyze existing results file"
    )

    args = parser.parse_args()

    # Run measurements
    if args.run_all or args.category == "pentest":
        harness = TestHarness(use_vps=args.vps, output_dir=args.output_dir)
        harness.run_all_pentest_tests()
        harness.print_summary()
        harness.save_results()

    elif args.analyze:
        # Analyze existing results
        try:
            with open(args.analyze) as f:
                measurements = json.load(f)

            print("\n=== TOKEN EFFICIENCY ANALYSIS ===\n")
            print(f"Analyzing {len(measurements)} measurements...\n")

            # Calculate statistics
            total_raw = sum(m["raw_tokens"] for m in measurements if not m.get("error"))
            total_minimal = sum(m["minimal_tokens"] for m in measurements if not m.get("error"))

            if total_raw > 0:
                avg_reduction = 100 * (1 - total_minimal / total_raw)
            else:
                avg_reduction = 0

            print(f"Average token reduction: {avg_reduction:.1f}%")
            print(f"Total raw tokens: {total_raw}")
            print(f"Total minimal tokens: {total_minimal}")

        except FileNotFoundError:
            print(f"[!] File not found: {args.analyze}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
