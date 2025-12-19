#!/usr/bin/env python3
"""
Test Suite for Progressive Context Loading Hooks

Tests all 4 hook scripts to ensure they function correctly:
1. load-framework-context.py (SessionStart)
2. detect-commands.py (UserPromptSubmit)
3. load-agent-skill-context.py (PreToolUse - Task)
4. update-session-state.py (Stop)

Usage:
    python hooks/test_hooks.py
    python hooks/test_hooks.py --verbose
    python hooks/test_hooks.py --test=1  # Run specific test
"""
import json
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Dict, Any


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class HookTester:
    """Test harness for hook scripts."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def run_hook(self, hook_path: str, input_data: Dict[str, Any]) -> Tuple[int, str, str]:
        """
        Run a hook script with given input data.

        Args:
            hook_path: Path to hook script
            input_data: Dictionary to send as JSON stdin

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["python", hook_path],
                input=json.dumps(input_data),
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # Replace decode errors with '?'
                timeout=10
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "ERROR: Hook execution timed out"
        except Exception as e:
            return -1, "", f"ERROR: {e}"

    def assert_contains(self, text: str, substring: str, message: str):
        """Assert that text contains substring."""
        if substring in text:
            self._pass(message)
        else:
            self._fail(f"{message}\n  Expected substring: '{substring}'\n  In text: '{text[:200]}...'")

    def assert_equals(self, actual: Any, expected: Any, message: str):
        """Assert that actual equals expected."""
        if actual == expected:
            self._pass(message)
        else:
            self._fail(f"{message}\n  Expected: {expected}\n  Got: {actual}")

    def assert_file_exists(self, file_path: Path, message: str):
        """Assert that file exists."""
        if file_path.exists():
            self._pass(message)
        else:
            self._fail(f"{message}\n  File not found: {file_path}")

    def _pass(self, message: str):
        """Record test pass."""
        self.tests_passed += 1
        self.tests_run += 1
        if self.verbose:
            print(f"  {Colors.GREEN}[PASS]{Colors.RESET} {message}")

    def _fail(self, message: str):
        """Record test failure."""
        self.tests_failed += 1
        self.tests_run += 1
        print(f"  {Colors.RED}[FAIL]{Colors.RESET} {message}")

    def test_header(self, test_name: str):
        """Print test header."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Test: {test_name}{Colors.RESET}")

    def summary(self):
        """Print test summary."""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}Test Summary{Colors.RESET}")
        print(f"  Total: {self.tests_run}")
        print(f"  {Colors.GREEN}Passed: {self.tests_passed}{Colors.RESET}")
        if self.tests_failed > 0:
            print(f"  {Colors.RED}Failed: {self.tests_failed}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] All tests passed!{Colors.RESET}")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}[ERROR] Some tests failed{Colors.RESET}")
            return 1


def test_1_load_framework_context(tester: HookTester):
    """Test 1: load-framework-context.py (SessionStart)"""
    tester.test_header("Test 1: Load Framework Context (SessionStart)")

    # Test 1.1: Hook executes successfully
    input_data = {
        "event": "SessionStart",
        "timestamp": "2025-12-12T10:00:00Z"
    }

    returncode, stdout, stderr = tester.run_hook("hooks/load-framework-context.py", input_data)
    tester.assert_equals(returncode, 0, "Hook exits with code 0")

    # Test 1.2: Output wrapped in <system-reminder> tags
    tester.assert_contains(stdout, "<system-reminder>", "Output contains opening <system-reminder> tag")
    tester.assert_contains(stdout, "</system-reminder>", "Output contains closing </system-reminder> tag")

    # Test 1.3: CLAUDE.md content included
    tester.assert_contains(stdout, "Intelligence Adjacent", "Output contains CLAUDE.md content")
    tester.assert_contains(stdout, "System Configuration", "Output contains CLAUDE.md sections")

    # Test 1.4: No errors in stderr
    tester.assert_equals(stderr.strip(), "", "No errors in stderr")


def test_2_detect_commands(tester: HookTester):
    """Test 2: detect-commands.py (UserPromptSubmit)"""
    tester.test_header("Test 2: Detect Commands (UserPromptSubmit)")

    # Test 2.1: Pentest keyword detection
    input_data = {
        "event": "UserPromptSubmit",
        "prompt": "I need to perform a pentest on example.com",
        "timestamp": "2025-12-12T10:05:00Z"
    }

    returncode, stdout, stderr = tester.run_hook("hooks/detect-commands.py", input_data)
    tester.assert_equals(returncode, 0, "Hook exits with code 0 (pentest)")
    tester.assert_contains(stdout, "/pentest", "Suggests /pentest command")

    # Test 2.2: Blog post keyword detection
    input_data["prompt"] = "Help me write a blog post about AI security"
    returncode, stdout, stderr = tester.run_hook("hooks/detect-commands.py", input_data)
    tester.assert_contains(stdout, "/blog-post", "Suggests /blog-post command")

    # Test 2.3: Job analysis keyword detection
    input_data["prompt"] = "I need to analyze a job posting for a security engineer role"
    returncode, stdout, stderr = tester.run_hook("hooks/detect-commands.py", input_data)
    tester.assert_contains(stdout, "/job-analysis", "Suggests /job-analysis command")

    # Test 2.4: No suggestion for irrelevant text
    input_data["prompt"] = "What is the weather today?"
    returncode, stdout, stderr = tester.run_hook("hooks/detect-commands.py", input_data)
    tester.assert_equals(stdout.strip(), "", "No suggestion for irrelevant text")

    # Test 2.5: Already a slash command - no suggestion
    input_data["prompt"] = "/pentest"
    returncode, stdout, stderr = tester.run_hook("hooks/detect-commands.py", input_data)
    tester.assert_equals(stdout.strip(), "", "No suggestion when user already typed slash command")


def test_3_load_agent_skill_context(tester: HookTester):
    """Test 3: load-agent-skill-context.py (PreToolUse - Task)"""
    tester.test_header("Test 3: Load Agent + Skill Context (PreToolUse)")

    # Test 3.1: Security agent loading
    input_data = {
        "event": "PreToolUse",
        "tool_name": "Task",
        "parameters": {
            "subagent_type": "security",
            "prompt": "Perform penetration test"
        },
        "timestamp": "2025-12-12T10:10:00Z"
    }

    returncode, stdout, stderr = tester.run_hook("hooks/load-agent-skill-context.py", input_data)
    tester.assert_equals(returncode, 0, "Hook exits with code 0 (security agent)")

    # Test 3.2: Agent prompt loaded
    tester.assert_contains(stdout, "=== AGENT PROMPT ===", "Output contains agent prompt section")
    tester.assert_contains(stdout, "Security Agent", "Agent prompt content loaded")

    # Test 3.3: Skill context loaded
    tester.assert_contains(stdout, "=== SKILL CONTEXT", "Output contains skill context section")
    tester.assert_contains(stdout, "security-testing", "Skill name in output")

    # Test 3.4: Tool catalog loaded
    tester.assert_contains(stdout, "=== TOOL CATALOG ===", "Output contains tool catalog section")

    # Test 3.5: Writer agent loading
    input_data["parameters"]["subagent_type"] = "writer"
    input_data["parameters"]["prompt"] = "Write blog post"
    returncode, stdout, stderr = tester.run_hook("hooks/load-agent-skill-context.py", input_data)
    tester.assert_contains(stdout, "Writer Agent", "Writer agent loaded")
    tester.assert_contains(stdout, "writer", "Writer skill loaded")

    # Test 3.6: Advisor agent - OSINT skill detection
    input_data["parameters"]["subagent_type"] = "advisor"
    input_data["parameters"]["prompt"] = "Research intelligence on APT group"
    returncode, stdout, stderr = tester.run_hook("hooks/load-agent-skill-context.py", input_data)
    tester.assert_contains(stdout, "osint-research", "OSINT skill loaded for advisor")


def test_4_update_session_state(tester: HookTester):
    """Test 4: update-session-state.py (Stop)"""
    tester.test_header("Test 4: Update Session State (Stop)")

    # Test 4.1: Session file creation
    input_data = {
        "event": "Stop",
        "session_duration": "30 minutes",
        "timestamp": "2025-12-12T10:30:00Z"
    }

    returncode, stdout, stderr = tester.run_hook("hooks/update-session-state.py", input_data)
    tester.assert_equals(returncode, 0, "Hook exits with code 0")

    # Test 4.2: Confirmation message
    tester.assert_contains(stdout, "Session state", "Confirmation message present")
    tester.assert_contains(stdout, "Session", "Session number mentioned")

    # Test 4.3: Session file exists
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    sessions_dir = Path("sessions")
    session_files = list(sessions_dir.glob(f"{today}-*.md"))
    tester.assert_file_exists(sessions_dir, "Sessions directory created")

    if session_files:
        # Test 4.4: Session file contains proper format
        session_file = session_files[0]
        content = session_file.read_text(encoding='utf-8')
        tester.assert_contains(content, "### Session", "Session entry format correct")
        tester.assert_contains(content, "**Context:**", "Context section present")
        tester.assert_contains(content, "**Next Actions:**", "Next Actions section present")


def test_5_integration_test(tester: HookTester):
    """Test 5: Integration test - All hooks together"""
    tester.test_header("Test 5: Integration Test")

    # Test 5.1: Verify all hook scripts exist
    hooks = [
        "hooks/load-framework-context.py",
        "hooks/detect-commands.py",
        "hooks/load-agent-skill-context.py",
        "hooks/update-session-state.py"
    ]

    for hook in hooks:
        tester.assert_file_exists(Path(hook), f"Hook exists: {hook}")

    # Test 5.2: Verify settings.json exists
    settings_file = Path(".claude/settings.json")
    tester.assert_file_exists(settings_file, "settings.json exists")

    if settings_file.exists():
        # Test 5.3: Verify settings.json structure
        settings = json.loads(settings_file.read_text(encoding='utf-8'))
        tester.assert_contains(str(settings), "SessionStart", "SessionStart hook configured")
        tester.assert_contains(str(settings), "UserPromptSubmit", "UserPromptSubmit hook configured")
        tester.assert_contains(str(settings), "PreToolUse", "PreToolUse hook configured")
        tester.assert_contains(str(settings), "Stop", "Stop hook configured")


def main():
    """Run all tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Test progressive context loading hooks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--test", "-t", type=int, help="Run specific test (1-5)")
    args = parser.parse_args()

    tester = HookTester(verbose=args.verbose)

    print(f"{Colors.BOLD}Progressive Context Loading - Hook Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

    # Run specific test or all tests
    if args.test == 1:
        test_1_load_framework_context(tester)
    elif args.test == 2:
        test_2_detect_commands(tester)
    elif args.test == 3:
        test_3_load_agent_skill_context(tester)
    elif args.test == 4:
        test_4_update_session_state(tester)
    elif args.test == 5:
        test_5_integration_test(tester)
    else:
        # Run all tests
        test_1_load_framework_context(tester)
        test_2_detect_commands(tester)
        test_3_load_agent_skill_context(tester)
        test_4_update_session_state(tester)
        test_5_integration_test(tester)

    tester.summary()
    return tester.tests_failed


if __name__ == "__main__":
    sys.exit(main())
