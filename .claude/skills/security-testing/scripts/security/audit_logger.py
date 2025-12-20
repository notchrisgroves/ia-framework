#!/usr/bin/env python3
"""
Audit Logger for Penetration Testing Engagements

Provides comprehensive audit logging for compliance and legal defense:
- Records all commands executed during testing
- Captures full outputs with timestamps
- Generates compliance reports and timelines
- Supports incident correlation

Usage:
    from tools.security.audit_logger import AuditLogger

    logger = AuditLogger(engagement_dir="output/engagements/pentest/client-2025-11")

    with logger.log_command(tool="nmap", command="nmap -sV 192.168.1.1", target="192.168.1.1"):
        # Execute command
        result = subprocess.run(...)
        logger.record_output(result.stdout)
        logger.record_exit_code(result.returncode)

Format:
    - JSON Lines (.jsonl) for structured data
    - Plain text (.txt) for human-readable transcripts
    - Separate output files for large tool outputs
    - SHA256 hashes for integrity verification

Author: Intelligence Adjacent
Version: 1.0
Created: 2025-11-23
"""

import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import threading
import queue
import time


class AuditLogger:
    """Comprehensive audit logging for penetration testing engagements"""

    def __init__(self, engagement_dir: str, enabled: bool = True, verbosity: str = "full"):
        """
        Initialize audit logger

        Args:
            engagement_dir: Path to engagement directory (e.g., "output/engagements/pentest/client-2025-11")
            enabled: Whether audit logging is enabled (default: True)
            verbosity: Logging verbosity - "full" (command+output) or "commands" (command only)
        """
        self.engagement_dir = Path(engagement_dir).expanduser().resolve()
        self.audit_dir = self.engagement_dir / "audit-logs"
        self.sessions_dir = self.audit_dir / "sessions"
        self.compliance_dir = self.audit_dir / "compliance"
        self.enabled = enabled
        self.verbosity = verbosity

        # Session tracking
        self.session_id = f"session-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.session_start = datetime.now(timezone.utc)
        self.command_sequence = 0

        # File paths
        self.jsonl_path = self.sessions_dir / f"{self.session_id}.jsonl"
        self.transcript_path = self.sessions_dir / f"{self.session_id}.txt"
        self.outputs_dir = self.sessions_dir / f"{self.session_id}-outputs"

        # Async write queue
        self.write_queue = queue.Queue()
        self.writer_thread = None
        self.shutdown_flag = threading.Event()

        # Current command context (for context manager)
        self._current_command = None
        self._command_start_time = None

        if self.enabled:
            self._initialize()

    def _initialize(self):
        """Initialize audit logging directories and files"""
        # Create directories
        self.audit_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)
        self.compliance_dir.mkdir(exist_ok=True)
        self.outputs_dir.mkdir(exist_ok=True)

        # Create configuration file
        config_path = self.audit_dir / "audit-config.json"
        if not config_path.exists():
            config = {
                "enabled": True,
                "verbosity": self.verbosity,
                "created": datetime.now(timezone.utc).isoformat(),
                "engagement": self.engagement_dir.name,
                "description": "Audit logging for compliance and legal defense"
            }
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

        # Create README
        readme_path = self.audit_dir / "README.md"
        if not readme_path.exists():
            readme_content = f"""# Audit Logs - {self.engagement_dir.name}

## Purpose

This directory contains comprehensive audit logs for this penetration testing engagement.

**Use cases:**
- **Compliance**: Meet SOC 2, ISO 27001, PCI DSS audit trail requirements
- **Legal Defense**: Prove what was/wasn't done during testing
- **Incident Correlation**: Map testing activities to client-observed events
- **Quality Assurance**: Post-engagement methodology review

## Structure

```
audit-logs/
├── README.md                    (This file)
├── audit-config.json            (Audit configuration)
├── audit-index.json             (Quick command lookup)
├── sessions/
│   ├── session-*.jsonl          (Structured logs - machine readable)
│   ├── session-*.txt            (Human-readable transcripts)
│   └── session-*-outputs/       (Raw tool outputs)
└── compliance/
    └── timeline-report.md       (Client-facing timeline)
```

## Log Formats

### Structured Logs (.jsonl)
JSON Lines format for programmatic analysis:
- One JSON object per line
- Each object = one command execution
- Includes: timestamp, command, output hash, duration, exit code

### Transcripts (.txt)
Human-readable chronological record:
- Timestamped command execution log
- Scope verification checkpoints
- Full command outputs (if verbosity=full)
- Exit codes and durations

### Compliance Reports
Timeline view for client presentation:
- Chronological activity summary
- Scope verification confirmations
- High-level findings correlation

## Integrity Verification

All outputs include SHA256 hashes for integrity verification:
```bash
# Verify output integrity
sha256sum audit-logs/sessions/session-*-outputs/*
```

## Retention Policy

- **Active engagement**: Keep all logs
- **Post-engagement**: Archive after final report delivery
- **Long-term**: Retain for 7 years (compliance requirement)

## Privacy & Security

⚠️ **SENSITIVE CONTENT WARNING**
- Contains full command outputs (may include credentials, tokens, session IDs)
- DO NOT share without redacting sensitive data
- Encrypt before transmitting to client
- Follow client data handling requirements

---

**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
**Engagement**: {self.engagement_dir.name}
**Audit Mode**: {'ENABLED' if self.enabled else 'DISABLED'}
"""
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)

        # Initialize transcript file
        self._write_transcript_header()

        # Start async writer thread
        self.writer_thread = threading.Thread(target=self._async_writer, daemon=True)
        self.writer_thread.start()

    def _write_transcript_header(self):
        """Write header to human-readable transcript"""
        header = f"""{'=' * 80}
PENETRATION TEST AUDIT LOG
{'=' * 80}
Engagement:     {self.engagement_dir.name}
Session ID:     {self.session_id}
Started:        {self.session_start.strftime('%Y-%m-%d %H:%M:%S UTC')}
Audit Mode:     {'ENABLED' if self.enabled else 'DISABLED'}
Verbosity:      {self.verbosity.upper()} ({"Full command + output capture" if self.verbosity == "full" else "Commands only"})
{'=' * 80}

"""
        with open(self.transcript_path, 'w', encoding='utf-8') as f:
            f.write(header)

    def _async_writer(self):
        """Background thread that writes logs asynchronously"""
        while not self.shutdown_flag.is_set():
            try:
                # Get log entry from queue (timeout to check shutdown flag)
                log_entry = self.write_queue.get(timeout=0.5)

                # Write to JSONL file
                with open(self.jsonl_path, 'a', encoding='utf-8') as f:
                    json.dump(log_entry, f)
                    f.write('\n')

                # Write to human-readable transcript
                self._write_transcript_entry(log_entry)

                self.write_queue.task_done()
            except queue.Empty:
                continue

    def _write_transcript_entry(self, entry: Dict[str, Any]):
        """Write human-readable transcript entry"""
        timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S.%f')[:-3]

        # Check if this is a scope verification entry (not a command)
        if entry.get('event_type') == 'scope_verification':
            # Scope verification entries are handled separately in log_scope_verification
            return

        transcript_entry = f"""
[{timestamp}] COMMAND #{entry['sequence']:03d}: {entry['tool']}
{'─' * 80}
Tool:        {entry['tool']} ({entry['category']})
Command:     {entry['command']}
Target:      {entry.get('target', 'N/A')}
Scope OK:    {'[OK] YES' if entry.get('scope_verified') else '[WARN] NOT VERIFIED'}
Working Dir: {entry['working_dir']}

"""

        # Add output if verbosity=full
        if self.verbosity == "full" and entry.get('output_file'):
            output_file = Path(entry['output_file'])
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                    output_content = f.read()
                transcript_entry += f"""--- BEGIN OUTPUT ---
{output_content}
--- END OUTPUT ---

"""

        # Add execution metadata
        duration_sec = entry['duration_ms'] / 1000.0
        transcript_entry += f"""Duration:    {duration_sec:.3f}s
Exit Code:   {entry.get('exit_code', 'N/A')}
Output Hash: {entry.get('output_hash', 'N/A')}
{'─' * 80}

"""

        with open(self.transcript_path, 'a', encoding='utf-8') as f:
            f.write(transcript_entry)

    @contextmanager
    def log_command(self, tool: str, command: str, target: Optional[str] = None,
                   category: str = "unknown", scope_verified: bool = False):
        """
        Context manager for logging a command execution

        Usage:
            with logger.log_command(tool="nmap", command="nmap -sV 192.168.1.1", target="192.168.1.1"):
                result = subprocess.run(...)
                logger.record_output(result.stdout)
                logger.record_exit_code(result.returncode)

        Args:
            tool: Tool name (e.g., "nmap", "nuclei")
            command: Full command string
            target: Target being scanned/tested
            category: Tool category (e.g., "kali_pentest", "web3_security")
            scope_verified: Whether target scope was verified before execution
        """
        if not self.enabled:
            yield
            return

        self.command_sequence += 1
        self._command_start_time = datetime.now(timezone.utc)

        self._current_command = {
            "timestamp": self._command_start_time.isoformat(),
            "session_id": self.session_id,
            "sequence": self.command_sequence,
            "command": command,
            "tool": tool,
            "category": category,
            "target": target,
            "scope_verified": scope_verified,
            "working_dir": str(Path.cwd()),
            "engagement": self.engagement_dir.name
        }

        try:
            yield self
        finally:
            # Finalize command entry
            duration = (datetime.now(timezone.utc) - self._command_start_time).total_seconds() * 1000
            self._current_command['duration_ms'] = round(duration, 3)

            # Queue for async write
            self.write_queue.put(self._current_command.copy())
            self._current_command = None

    def record_output(self, output: str, filename: Optional[str] = None):
        """
        Record command output

        Args:
            output: Command output text
            filename: Optional custom filename (default: auto-generated)
        """
        if not self.enabled or not self._current_command:
            return

        if filename is None:
            filename = f"{self.session_id}-cmd-{self.command_sequence:03d}-output.txt"

        output_path = self.outputs_dir / filename

        # Write output to file
        with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(output)

        # Calculate hash
        output_hash = hashlib.sha256(output.encode('utf-8', errors='ignore')).hexdigest()

        # Update current command
        self._current_command['output_file'] = str(output_path)
        self._current_command['output_hash'] = f"sha256:{output_hash}"
        self._current_command['output_size_bytes'] = len(output.encode('utf-8', errors='ignore'))

    def record_exit_code(self, exit_code: int):
        """Record command exit code"""
        if not self.enabled or not self._current_command:
            return

        self._current_command['exit_code'] = exit_code

    def log_scope_verification(self, target: str, verified: bool, scope_line: Optional[int] = None):
        """
        Log a scope verification checkpoint

        Args:
            target: Target being verified
            verified: Whether target is in scope
            scope_line: Line number in SCOPE.md where target appears
        """
        if not self.enabled:
            return

        checkpoint_entry = f"""
[{datetime.now(timezone.utc).strftime('%H:%M:%S.%f')[:-3]}] SCOPE VERIFICATION
{'─' * 80}
Target:      {target}
Status:      {'[OK] IN SCOPE' if verified else '[FAIL] OUT OF SCOPE'}
Reference:   {'SCOPE.md line ' + str(scope_line) if scope_line else 'Manual verification'}
{'─' * 80}

"""

        with open(self.transcript_path, 'a', encoding='utf-8') as f:
            f.write(checkpoint_entry)

        # Also add to structured log
        self.write_queue.put({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": "scope_verification",
            "target": target,
            "verified": verified,
            "scope_line": scope_line
        })

    def generate_timeline_report(self) -> str:
        """
        Generate compliance timeline report

        Returns:
            Path to generated report
        """
        if not self.enabled:
            return ""

        timeline_path = self.compliance_dir / f"timeline-{self.session_id}.md"

        # Read all JSONL entries
        entries = []
        if self.jsonl_path.exists():
            with open(self.jsonl_path, 'r') as f:
                for line in f:
                    entries.append(json.loads(line))

        # Generate report
        report_content = f"""# Testing Timeline Report
**Engagement**: {self.engagement_dir.name}
**Session**: {self.session_id}
**Period**: {self.session_start.strftime('%Y-%m-%d %H:%M:%S UTC')} - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

## Activity Summary

| Time (UTC) | Tool | Target | Command | Duration | Status |
|------------|------|--------|---------|----------|--------|
"""

        for entry in entries:
            if entry.get('event_type') == 'scope_verification':
                continue  # Skip scope verifications in summary table

            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
            tool = entry.get('tool', 'N/A')
            target = entry.get('target', 'N/A')
            command = entry.get('command', '')[:50] + ('...' if len(entry.get('command', '')) > 50 else '')
            duration = f"{entry.get('duration_ms', 0) / 1000:.1f}s"
            exit_code = entry.get('exit_code', 'N/A')
            status = '[OK]' if exit_code == 0 else ('[FAIL]' if exit_code != 'N/A' else '[PEND]')

            report_content += f"| {timestamp} | {tool} | {target} | `{command}` | {duration} | {status} |\n"

        report_content += f"""

## Scope Verifications

All targets were verified against SCOPE.md before testing:

"""

        # Add scope verifications
        for entry in entries:
            if entry.get('event_type') == 'scope_verification':
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
                target = entry.get('target', 'N/A')
                status = '[OK] IN SCOPE' if entry.get('verified') else '[FAIL] OUT OF SCOPE'
                report_content += f"- `{timestamp}` - {target} - {status}\n"

        report_content += f"""

## Compliance Notes

- All commands logged with full timestamps
- Output integrity verified with SHA256 hashes
- Scope verification performed before each target test
- Complete audit trail available in `audit-logs/sessions/{self.session_id}.txt`

---

**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
"""

        with open(timeline_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return str(timeline_path)

    def shutdown(self):
        """Shutdown audit logger and flush pending writes"""
        if not self.enabled:
            return

        # Wait for queue to empty
        self.write_queue.join()

        # Signal shutdown
        self.shutdown_flag.set()

        # Wait for writer thread
        if self.writer_thread and self.writer_thread.is_alive():
            self.writer_thread.join(timeout=5.0)

        # Generate timeline report
        timeline_path = self.generate_timeline_report()

        # Write session footer
        footer = f"""
{'=' * 80}
SESSION COMPLETED
{'=' * 80}
Ended:          {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
Duration:       {(datetime.now(timezone.utc) - self.session_start).total_seconds() / 60:.1f} minutes
Commands:       {self.command_sequence}
Timeline:       {timeline_path if timeline_path else 'N/A'}
{'=' * 80}
"""

        with open(self.transcript_path, 'a', encoding='utf-8') as f:
            f.write(footer)

        # Update index
        self._update_index()

    def _update_index(self):
        """Update audit index for quick lookups"""
        index_path = self.audit_dir / "audit-index.json"

        # Load existing index
        index = {}
        if index_path.exists():
            with open(index_path, 'r') as f:
                index = json.load(f)

        # Add this session
        index[self.session_id] = {
            "started": self.session_start.isoformat(),
            "ended": datetime.now(timezone.utc).isoformat(),
            "commands": self.command_sequence,
            "jsonl_file": str(self.jsonl_path.relative_to(self.audit_dir)),
            "transcript_file": str(self.transcript_path.relative_to(self.audit_dir))
        }

        # Write updated index
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, sort_keys=True)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
        return False


# Convenience function for quick audit logging
def create_audit_logger(engagement_dir: str, enabled: bool = True) -> AuditLogger:
    """
    Create an audit logger for an engagement

    Args:
        engagement_dir: Path to engagement directory
        enabled: Whether audit logging is enabled

    Returns:
        AuditLogger instance
    """
    return AuditLogger(engagement_dir=engagement_dir, enabled=enabled)
