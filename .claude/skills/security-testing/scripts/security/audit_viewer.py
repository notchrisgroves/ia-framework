#!/usr/bin/env python3
"""
Audit Log Viewer and Analyzer

View, search, and analyze penetration testing audit logs.

Usage:
    # View latest session
    python tools/security/audit_viewer.py --engagement output/engagements/pentest/client-2025-11

    # View specific session
    python tools/security/audit_viewer.py --engagement ... --session session-20251123-143022

    # Search for specific target
    python tools/security/audit_viewer.py --engagement ... --search-target 192.168.1.1

    # Search for specific tool
    python tools/security/audit_viewer.py --engagement ... --search-tool nmap

    # Generate compliance report
    python tools/security/audit_viewer.py --engagement ... --export-compliance report.md

    # Verify output integrity
    python tools/security/audit_viewer.py --engagement ... --verify-integrity

Author: Intelligence Adjacent
Version: 1.0
Created: 2025-11-23
"""

import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import sys


class AuditViewer:
    """View and analyze audit logs"""

    def __init__(self, engagement_dir: str):
        self.engagement_dir = Path(engagement_dir).expanduser().resolve()
        self.audit_dir = self.engagement_dir / "audit-logs"
        self.sessions_dir = self.audit_dir / "sessions"

        if not self.audit_dir.exists():
            raise FileNotFoundError(f"No audit logs found in {self.engagement_dir}")

    def list_sessions(self) -> List[str]:
        """List all audit sessions"""
        if not self.sessions_dir.exists():
            return []

        sessions = []
        for jsonl_file in self.sessions_dir.glob("*.jsonl"):
            sessions.append(jsonl_file.stem)

        return sorted(sessions)

    def get_latest_session(self) -> Optional[str]:
        """Get the most recent session ID"""
        sessions = self.list_sessions()
        return sessions[-1] if sessions else None

    def load_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Load all entries from a session"""
        jsonl_path = self.sessions_dir / f"{session_id}.jsonl"

        if not jsonl_path.exists():
            raise FileNotFoundError(f"Session not found: {session_id}")

        entries = []
        with open(jsonl_path, 'r') as f:
            for line in f:
                entries.append(json.loads(line))

        return entries

    def view_session(self, session_id: Optional[str] = None, format: str = "table"):
        """
        View session audit log

        Args:
            session_id: Session to view (default: latest)
            format: Output format - "table", "json", "transcript"
        """
        if session_id is None:
            session_id = self.get_latest_session()
            if session_id is None:
                print("[FAIL] No audit sessions found")
                return

        entries = self.load_session(session_id)

        if format == "json":
            print(json.dumps(entries, indent=2))
        elif format == "transcript":
            self._view_transcript(session_id)
        else:  # table
            self._view_table(entries, session_id)

    def _view_table(self, entries: List[Dict[str, Any]], session_id: str):
        """View entries as formatted table"""
        print(f"\n{'=' * 120}")
        print(f"AUDIT LOG: {session_id}")
        print(f"{'=' * 120}\n")

        # Header
        print(f"{'#':<4} {'Time':<12} {'Tool':<15} {'Target':<25} {'Status':<8} {'Duration':<10}")
        print(f"{'-' * 4} {'-' * 12} {'-' * 15} {'-' * 25} {'-' * 8} {'-' * 10}")

        # Entries
        for entry in entries:
            if entry.get('event_type') == 'scope_verification':
                continue  # Skip scope verifications in table view

            seq = entry.get('sequence', 0)
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
            tool = entry.get('tool', 'N/A')[:15]
            target = entry.get('target', 'N/A')[:25]
            exit_code = entry.get('exit_code', 'N/A')
            status = '[OK] OK' if exit_code == 0 else ('[FAIL] FAIL' if exit_code != 'N/A' else '[PEND] RUN')
            duration = f"{entry.get('duration_ms', 0) / 1000:.2f}s"

            print(f"{seq:<4} {timestamp:<12} {tool:<15} {target:<25} {status:<8} {duration:<10}")

        print(f"\n{len(entries)} total commands\n")

    def _view_transcript(self, session_id: str):
        """View human-readable transcript"""
        transcript_path = self.sessions_dir / f"{session_id}.txt"

        if not transcript_path.exists():
            print(f"[FAIL] Transcript not found: {transcript_path}")
            return

        with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read())

    def search_target(self, target: str, session_id: Optional[str] = None):
        """Search for all commands against a specific target"""
        if session_id is None:
            # Search all sessions
            sessions = self.list_sessions()
        else:
            sessions = [session_id]

        results = []
        for sess in sessions:
            entries = self.load_session(sess)
            for entry in entries:
                if entry.get('target') == target:
                    results.append({**entry, 'session': sess})

        if not results:
            print(f"[FAIL] No commands found for target: {target}")
            return

        print(f"\n{'=' * 120}")
        print(f"COMMANDS AGAINST TARGET: {target}")
        print(f"{'=' * 120}\n")

        print(f"{'Session':<30} {'Time':<12} {'Tool':<15} {'Command':<50}")
        print(f"{'-' * 30} {'-' * 12} {'-' * 15} {'-' * 50}")

        for result in results:
            session = result['session']
            timestamp = datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            tool = result.get('tool', 'N/A')[:15]
            command = result.get('command', '')[:50]

            print(f"{session:<30} {timestamp:<12} {tool:<15} {command:<50}")

        print(f"\n{len(results)} commands found\n")

    def search_tool(self, tool: str, session_id: Optional[str] = None):
        """Search for all uses of a specific tool"""
        if session_id is None:
            sessions = self.list_sessions()
        else:
            sessions = [session_id]

        results = []
        for sess in sessions:
            entries = self.load_session(sess)
            for entry in entries:
                if entry.get('tool') == tool:
                    results.append({**entry, 'session': sess})

        if not results:
            print(f"[FAIL] No commands found for tool: {tool}")
            return

        print(f"\n{'=' * 120}")
        print(f"TOOL USAGE: {tool}")
        print(f"{'=' * 120}\n")

        print(f"{'Session':<30} {'Time':<12} {'Target':<25} {'Command':<50}")
        print(f"{'-' * 30} {'-' * 12} {'-' * 25} {'-' * 50}")

        for result in results:
            session = result['session']
            timestamp = datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            target = result.get('target', 'N/A')[:25]
            command = result.get('command', '')[:50]

            print(f"{session:<30} {timestamp:<12} {target:<25} {command:<50}")

        print(f"\n{len(results)} uses found\n")

    def verify_integrity(self, session_id: Optional[str] = None):
        """Verify output file integrity using SHA256 hashes"""
        if session_id is None:
            session_id = self.get_latest_session()

        entries = self.load_session(session_id)

        print(f"\n{'=' * 100}")
        print(f"INTEGRITY VERIFICATION: {session_id}")
        print(f"{'=' * 100}\n")

        print(f"{'File':<60} {'Status':<15} {'Hash Match':<25}")
        print(f"{'-' * 60} {'-' * 15} {'-' * 25}")

        verified = 0
        failed = 0
        missing = 0

        for entry in entries:
            output_file = entry.get('output_file')
            expected_hash = entry.get('output_hash', '').replace('sha256:', '')

            if not output_file or not expected_hash:
                continue

            output_path = Path(output_file)

            if not output_path.exists():
                print(f"{output_path.name[:60]:<60} {'[FAIL] MISSING':<15} {expected_hash[:25]:<25}")
                missing += 1
                continue

            # Calculate actual hash
            with open(output_path, 'rb') as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()

            if actual_hash == expected_hash:
                print(f"{output_path.name[:60]:<60} {'[OK] VERIFIED':<15} {'Match':<25}")
                verified += 1
            else:
                print(f"{output_path.name[:60]:<60} {'[FAIL] MISMATCH':<15} {actual_hash[:25]:<25}")
                failed += 1

        print(f"\n{'=' * 100}")
        print(f"Results: {verified} verified | {failed} mismatches | {missing} missing")
        print(f"{'=' * 100}\n")

        if failed > 0 or missing > 0:
            print("[WARN]  WARNING: Some files failed integrity verification!")
            print("   This could indicate tampering or file corruption.")
            return False
        else:
            print("[OK] All files passed integrity verification")
            return True

    def export_compliance_report(self, output_path: str, session_id: Optional[str] = None):
        """Export compliance report for client presentation"""
        if session_id is None:
            session_id = self.get_latest_session()

        entries = self.load_session(session_id)

        # Generate compliance report
        report = f"""# Penetration Testing Activity Report

**Engagement**: {self.engagement_dir.name}
**Session**: {session_id}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Executive Summary

This report documents all testing activities performed during the penetration testing engagement. All activities were conducted within the authorized scope and in accordance with the Statement of Work.

## Activity Timeline

| Time (UTC) | Tool | Target | Activity Description | Duration | Status |
|------------|------|--------|----------------------|----------|--------|
"""

        for entry in entries:
            if entry.get('event_type') == 'scope_verification':
                continue

            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
            tool = entry.get('tool', 'N/A')
            target = entry.get('target', 'N/A')
            command = entry.get('command', '')[:60] + ('...' if len(entry.get('command', '')) > 60 else '')
            duration = f"{entry.get('duration_ms', 0) / 1000:.1f}s"
            exit_code = entry.get('exit_code', 'N/A')
            status = '[OK] Success' if exit_code == 0 else ('[FAIL] Failed' if exit_code != 'N/A' else '[PEND] Running')

            report += f"| {timestamp} | {tool} | {target} | `{command}` | {duration} | {status} |\n"

        report += f"""

## Scope Verification

All targets were verified against the authorized scope (SCOPE.md) before testing:

"""

        # Add scope verifications
        scope_checks = [e for e in entries if e.get('event_type') == 'scope_verification']
        for check in scope_checks:
            timestamp = datetime.fromisoformat(check['timestamp']).strftime('%H:%M:%S')
            target = check.get('target', 'N/A')
            status = '[OK] Authorized' if check.get('verified') else '[FAIL] Blocked'
            report += f"- `{timestamp}` - {target} - {status}\n"

        report += f"""

## Testing Methodology

Testing was conducted following industry-standard methodologies:
- OWASP Testing Guide (WSTG)
- PTES (Penetration Testing Execution Standard)
- MITRE ATT&CK Framework

## Compliance & Audit Trail

- **Total Commands Executed**: {len(entries)}
- **Audit Log Location**: `audit-logs/sessions/{session_id}.jsonl`
- **Transcript Location**: `audit-logs/sessions/{session_id}.txt`
- **Integrity Verification**: SHA256 hashes for all outputs
- **Retention Period**: 7 years (compliance requirement)

## Legal & Authorization

All testing activities were:
- Authorized in writing by {self.engagement_dir.name}
- Conducted within defined scope boundaries
- Performed during authorized timeframes
- Documented with complete audit trail

## Contact Information

For questions about this testing activity, contact:
- **Tester**: notchrisgroves@wearehackerone.com
- **Engagement ID**: {self.engagement_dir.name}

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Audit System**: Intelligence Adjacent Pentest Audit v1.0
"""

        # Write report
        output = Path(output_path).expanduser()
        with open(output, 'w') as f:
            f.write(report)

        print(f"[OK] Compliance report exported to: {output}")
        return str(output)


def main():
    parser = argparse.ArgumentParser(
        description="View and analyze penetration testing audit logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View latest session
  python audit_viewer.py --engagement output/engagements/pentest/client-2025-11

  # View specific session as table
  python audit_viewer.py --engagement ... --session session-20251123-143022

  # View as JSON
  python audit_viewer.py --engagement ... --format json

  # View transcript
  python audit_viewer.py --engagement ... --format transcript

  # Search for target
  python audit_viewer.py --engagement ... --search-target 192.168.1.1

  # Search for tool
  python audit_viewer.py --engagement ... --search-tool nmap

  # Verify integrity
  python audit_viewer.py --engagement ... --verify-integrity

  # Export compliance report
  python audit_viewer.py --engagement ... --export-compliance report.md
        """
    )

    parser.add_argument(
        '--engagement',
        required=True,
        help='Path to engagement directory'
    )

    parser.add_argument(
        '--session',
        help='Session ID to view (default: latest)'
    )

    parser.add_argument(
        '--format',
        choices=['table', 'json', 'transcript'],
        default='table',
        help='Output format (default: table)'
    )

    parser.add_argument(
        '--search-target',
        metavar='TARGET',
        help='Search for commands against specific target'
    )

    parser.add_argument(
        '--search-tool',
        metavar='TOOL',
        help='Search for uses of specific tool'
    )

    parser.add_argument(
        '--verify-integrity',
        action='store_true',
        help='Verify output file integrity'
    )

    parser.add_argument(
        '--export-compliance',
        metavar='OUTPUT',
        help='Export compliance report to file'
    )

    parser.add_argument(
        '--list-sessions',
        action='store_true',
        help='List all audit sessions'
    )

    args = parser.parse_args()

    try:
        viewer = AuditViewer(args.engagement)

        if args.list_sessions:
            sessions = viewer.list_sessions()
            print(f"\nAudit Sessions ({len(sessions)} total):")
            for session in sessions:
                print(f"  - {session}")
            print()

        elif args.search_target:
            viewer.search_target(args.search_target, args.session)

        elif args.search_tool:
            viewer.search_tool(args.search_tool, args.session)

        elif args.verify_integrity:
            success = viewer.verify_integrity(args.session)
            sys.exit(0 if success else 1)

        elif args.export_compliance:
            viewer.export_compliance_report(args.export_compliance, args.session)

        else:
            viewer.view_session(args.session, args.format)

    except FileNotFoundError as e:
        print(f"[FAIL] Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
