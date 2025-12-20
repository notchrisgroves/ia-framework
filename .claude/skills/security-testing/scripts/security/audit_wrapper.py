#!/usr/bin/env python3
"""
Audit Wrapper for Security Tools

Wraps security tool executions to provide comprehensive audit logging.
Works with Code API wrappers (servers/*/*) to log all commands and outputs.

Usage:
    from tools.security.audit_wrapper import with_audit_logging

    @with_audit_logging(tool="nmap", category="kali_pentest")
    def nmap(target, options, engagement_dir):
        # Original tool logic
        ...

Or use directly:

    from tools.security.audit_wrapper import execute_with_audit

    result = execute_with_audit(
        tool="nmap",
        category="kali_pentest",
        command=f"nmap {options} {target}",
        target=target,
        engagement_dir=engagement_dir,
        execution_func=lambda: actual_nmap_execution()
    )

Author: Intelligence Adjacent
Version: 1.0
Created: 2025-11-23
"""

import os
import functools
from pathlib import Path
from typing import Callable, Any, Dict, Optional
from tools.security.audit_logger import AuditLogger


# Global audit logger instance (initialized per engagement)
_audit_logger_instance = None
_audit_enabled = False


def initialize_audit_logging(engagement_dir: str, enabled: bool = True):
    """
    Initialize audit logging for an engagement

    This should be called at the start of each penetration testing session.

    Args:
        engagement_dir: Path to engagement directory
        enabled: Whether audit logging is enabled
    """
    global _audit_logger_instance, _audit_enabled

    _audit_enabled = enabled

    if enabled:
        _audit_logger_instance = AuditLogger(
            engagement_dir=engagement_dir,
            enabled=True,
            verbosity="full"
        )
        print(f"[OK] Audit logging ENABLED for {Path(engagement_dir).name}")
        print(f"   Logs: {Path(engagement_dir) / 'audit-logs' / 'sessions'}")
    else:
        _audit_logger_instance = None
        print(f"[WARN] Audit logging DISABLED for {Path(engagement_dir).name}")


def shutdown_audit_logging():
    """Shutdown audit logging and generate final reports"""
    global _audit_logger_instance, _audit_enabled

    if _audit_enabled and _audit_logger_instance:
        print("\n[AUDIT] Generating compliance reports...")
        _audit_logger_instance.shutdown()
        print("[OK] Audit logging session closed")

    _audit_logger_instance = None
    _audit_enabled = False


def is_audit_enabled() -> bool:
    """Check if audit logging is currently enabled"""
    return _audit_enabled and _audit_logger_instance is not None


def log_scope_verification(target: str, verified: bool, scope_line: Optional[int] = None):
    """
    Log a scope verification checkpoint

    Args:
        target: Target being verified
        verified: Whether target is in scope
        scope_line: Line number in SCOPE.md where target appears
    """
    if _audit_enabled and _audit_logger_instance:
        _audit_logger_instance.log_scope_verification(target, verified, scope_line)


def execute_with_audit(
    tool: str,
    category: str,
    command: str,
    target: Optional[str],
    engagement_dir: str,
    execution_func: Callable[[], Dict[str, Any]],
    scope_verified: bool = False
) -> Dict[str, Any]:
    """
    Execute a security tool with audit logging

    Args:
        tool: Tool name (e.g., "nmap", "nuclei")
        category: Tool category (e.g., "kali_pentest", "web3_security")
        command: Full command string
        target: Target being scanned/tested
        engagement_dir: Path to engagement directory
        execution_func: Function that executes the actual tool
        scope_verified: Whether target scope was verified

    Returns:
        Result from execution_func
    """
    # Check if audit logging is enabled
    if not _audit_enabled or not _audit_logger_instance:
        # No audit logging - execute normally
        return execution_func()

    # Execute with audit logging
    with _audit_logger_instance.log_command(
        tool=tool,
        command=command,
        target=target,
        category=category,
        scope_verified=scope_verified
    ):
        # Execute tool
        result = execution_func()

        # Record output and exit code
        if isinstance(result, dict):
            # Standard Code API wrapper format
            if 'output' in result:
                _audit_logger_instance.record_output(result['output'])
            elif 'message' in result:
                _audit_logger_instance.record_output(result['message'])

            # Record exit code if available
            if 'success' in result:
                _audit_logger_instance.record_exit_code(0 if result['success'] else 1)

        return result


def with_audit_logging(tool: str, category: str):
    """
    Decorator to add audit logging to security tools

    Usage:
        @with_audit_logging(tool="nmap", category="kali_pentest")
        def nmap(target, options, engagement_dir):
            # Tool implementation
            ...

    Args:
        tool: Tool name
        category: Tool category
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract common parameters
            target = kwargs.get('target') or (args[0] if len(args) > 0 else None)
            options = kwargs.get('options') or (args[1] if len(args) > 1 else '')
            engagement_dir = kwargs.get('engagement_dir') or (args[2] if len(args) > 2 else None)
            scope_verified = kwargs.get('scope_verified', False)

            # Build command string
            command = f"{tool} {options} {target}" if target else f"{tool} {options}"

            # Execute with audit logging
            return execute_with_audit(
                tool=tool,
                category=category,
                command=command,
                target=target,
                engagement_dir=engagement_dir or os.getcwd(),
                execution_func=lambda: func(*args, **kwargs),
                scope_verified=scope_verified
            )

        return wrapper
    return decorator


# Context manager for audit sessions
class AuditSession:
    """
    Context manager for audit logging sessions

    Usage:
        with AuditSession(engagement_dir="...", enabled=True):
            # All tool executions will be audited
            result = nmap.nmap(target="192.168.1.1", options="-sV", engagement_dir="...")
    """

    def __init__(self, engagement_dir: str, enabled: bool = True):
        self.engagement_dir = engagement_dir
        self.enabled = enabled

    def __enter__(self):
        initialize_audit_logging(self.engagement_dir, self.enabled)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutdown_audit_logging()
        return False
