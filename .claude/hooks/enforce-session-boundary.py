#!/usr/bin/env python3
"""
PostToolUse Hook: Enforce session boundary with /clear suggestions

Trigger: PostToolUse (after any tool completes)
Purpose: Monitor for task completion signals and suggest checkpoint + /clear workflow
Output: <system-reminder> with session boundary suggestions when appropriate
"""
import json
import sys
import io
from pathlib import Path
from datetime import datetime

# Ensure stdout uses UTF-8 encoding (Windows fix)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def count_messages_in_session():
    """
    Estimate message count from conversation (approximate).

    Returns:
        Estimated message count or None if unavailable
    """
    # This is approximate - actual message counting would require
    # tracking via a persistent counter file
    # For MVP, we'll return None and rely on other signals
    return None


def get_active_session_file():
    """
    Find today's active session file if it exists.

    Returns:
        Path to session file or None if no active session
    """
    sessions_dir = Path("sessions")
    if not sessions_dir.exists():
        return None

    today = datetime.now().strftime("%Y-%m-%d")
    existing_files = list(sessions_dir.glob(f"{today}-*.md"))

    if existing_files:
        # Return most recently modified
        return max(existing_files, key=lambda p: p.stat().st_mtime)

    return None


def check_todo_completion(data):
    """
    Check if tool use suggests task completion.

    Looks for:
    - TodoWrite tool with all completed tasks
    - Write/Edit to session files
    - Commit messages suggesting completion

    Args:
        data: Hook data from stdin

    Returns:
        Boolean indicating if tasks appear complete
    """
    tool_name = data.get("name", "")
    tool_input = data.get("input", {})

    # Check if TodoWrite with all completed
    if tool_name == "TodoWrite":
        todos = tool_input.get("todos", [])
        if todos:
            all_complete = all(t.get("status") == "completed" for t in todos)
            if all_complete and len(todos) >= 3:  # At least 3 tasks completed
                return True

    # Check if committing work (suggests completion)
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if "git commit" in command and ("complete" in command.lower() or "finish" in command.lower()):
            return True

    return False


def should_suggest_clear(data):
    """
    Determine if we should suggest /clear + checkpoint workflow.

    Args:
        data: Hook data from stdin

    Returns:
        Tuple of (should_suggest: bool, reason: str)
    """
    # Check for task completion signals
    if check_todo_completion(data):
        return True, "All tasks marked as completed"

    # Check message count (if available)
    message_count = count_messages_in_session()
    if message_count and message_count > 100:
        return True, f"Session has {message_count}+ messages (context may be bloated)"

    return False, ""


def create_suggestion_message(reason, session_file):
    """
    Create the suggestion message for session boundary.

    Args:
        reason: Why we're suggesting /clear
        session_file: Path to active session file (or None)

    Returns:
        Formatted suggestion message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    message_lines = [
        "<system-reminder>",
        f"🔄 SESSION BOUNDARY DETECTED ({timestamp})",
        f"Reason: {reason}",
        "",
        "**Recommended Workflow:**",
        "1. Review work completed this session",
    ]

    if session_file:
        message_lines.extend([
            f"2. Update session file: {session_file.name}",
            "   - Add session entry with completed tasks",
            "   - List files created/modified",
            "   - Update 'Next Actions' section",
        ])
    else:
        message_lines.extend([
            "2. Create session file if this is multi-session work:",
            "   - Location: sessions/YYYY-MM-DD-project-name.md",
            "   - Use template: library/templates/SESSION-STATE-TEMPLATE.md",
        ])

    message_lines.extend([
        "3. Run: /clear (clears context, starts fresh session)",
        "4. To resume: Read the session file listed above for context",
        "",
        "**Benefits of /clear between tasks:**",
        "- Reduces token usage by 80%+",
        "- Prevents context drift and confusion",
        "- Keeps sessions focused on single tasks",
        "- Makes resumption faster and clearer",
        "",
        "**IMPORTANT:**",
        "- Session file is your single source of truth",
        "- Do NOT create duplicate tracking files (STATUS.md, COMPLETE.md, etc.)",
        "- Update the SAME session file across multiple sessions",
        "",
        "</system-reminder>"
    ])

    return "\n".join(message_lines)


def main():
    """Monitor for session boundary signals and suggest /clear workflow."""
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Check if we should suggest /clear
        should_suggest, reason = should_suggest_clear(data)

        if should_suggest:
            # Find active session file
            session_file = get_active_session_file()

            # Create and output suggestion
            message = create_suggestion_message(reason, session_file)
            print(message)

        # Always exit 0 (don't block workflow)
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON from stdin: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"ERROR in enforce-session-boundary: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
