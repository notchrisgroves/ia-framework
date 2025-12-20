#!/usr/bin/env python3
"""
Stop Hook: Auto-update SESSION-STATE.md on session end

Trigger: Stop (session end, user closes conversation)
Purpose: Automatically append session summary to SESSION-STATE.md
Output: Confirmation message wrapped in <system-reminder>

Enhanced with automatic capture:
- Git commit messages from today
- Modified files summary
- Uncommitted changes summary
"""
import json
import sys
import io
import subprocess
from pathlib import Path
from datetime import datetime

# Ensure stdout uses UTF-8 encoding (Windows fix)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_or_create_session_file():
    """
    Find or create today's session state file.

    Returns:
        Tuple of (session_file_path, session_number, is_new_file)
    """
    sessions_dir = Path("sessions")
    sessions_dir.mkdir(exist_ok=True)

    # Look for today's session file
    today = datetime.now().strftime("%Y-%m-%d")
    existing_files = list(sessions_dir.glob(f"{today}-*.md"))

    if existing_files:
        # Use most recently modified file
        session_file = max(existing_files, key=lambda p: p.stat().st_mtime)

        # Parse session number from file
        content = session_file.read_text(encoding='utf-8')
        # Count existing session entries
        session_count = content.count("### Session ")
        return session_file, session_count + 1, False

    # No existing file - create new one
    project_name = "framework-work"  # Default name
    session_file = sessions_dir / f"{today}-{project_name}.md"

    # Create initial file
    initial_content = f"""# Session State: {project_name}

**Project:** IA Framework Development
**Date:** {today}
**Status:** Active

---

## Session History

"""
    session_file.write_text(initial_content, encoding='utf-8')
    return session_file, 1, True


def get_modified_files():
    """
    Get list of modified files using git.

    Returns:
        List of modified file paths, or None if git unavailable
    """
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            # Git short status format: "XY filename" where XY is 2-char status + space
            files = [line[3:].strip() for line in lines if len(line) > 3]
            return files if files else []
    except Exception:
        return None


def get_todays_commits():
    """
    Get commit messages from today.

    Returns:
        List of commit message strings, or empty list if unavailable
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        result = subprocess.run(
            ["git", "log", "--oneline", f"--since={today} 00:00:00", "--format=%s"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            commits = result.stdout.strip().split("\n")
            return [c for c in commits if c and not c.startswith("Merge")]
    except Exception:
        pass
    return []


def get_files_changed_today():
    """
    Get summary of files changed in today's commits.

    Returns:
        Dict with counts by directory, or None if unavailable
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        result = subprocess.run(
            ["git", "log", "--name-only", "--pretty=format:", f"--since={today} 00:00:00"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            files = [f for f in result.stdout.strip().split("\n") if f]
            # Group by top-level directory
            dirs = {}
            for f in files:
                top_dir = f.split("/")[0] if "/" in f else "(root)"
                dirs[top_dir] = dirs.get(top_dir, 0) + 1
            return dirs
    except Exception:
        pass
    return None


def create_session_entry(session_number, data):
    """
    Create session entry markdown with automatic capture.

    Args:
        session_number: Session number (int)
        data: Hook data from stdin (dict)

    Returns:
        Session entry markdown (string)
    """
    now = datetime.now()
    timestamp = now.strftime("%H:%M")
    date = now.strftime("%Y-%m-%d")

    # Gather automatic data
    modified_files = get_modified_files()
    todays_commits = get_todays_commits()
    files_by_dir = get_files_changed_today()

    # Build session entry
    entry_lines = [
        f"### Session {session_number} - {date} {timestamp}",
        "",
    ]

    # Add commits as work summary (automatic)
    if todays_commits:
        entry_lines.append("**Work Completed:**")
        for commit in todays_commits[:8]:  # Limit to 8 commits
            # Clean up commit message for display
            clean_msg = commit.replace("Feature: ", "").replace("Fix: ", "").replace("Cleanup: ", "")
            entry_lines.append(f"- {clean_msg}")
        if len(todays_commits) > 8:
            entry_lines.append(f"- ... and {len(todays_commits) - 8} more commits")
        entry_lines.append("")
    else:
        entry_lines.extend([
            "**Work Completed:**",
            "- [No commits - fill in manually]",
            ""
        ])

    # Add files changed by directory (automatic)
    if files_by_dir:
        entry_lines.append("**Areas Modified:**")
        for dir_name, count in sorted(files_by_dir.items(), key=lambda x: -x[1])[:5]:
            entry_lines.append(f"- {dir_name}/ ({count} files)")
        entry_lines.append("")

    # Add uncommitted changes if any
    if modified_files:
        entry_lines.append("**Uncommitted Changes:**")
        for file in modified_files[:5]:  # Limit to 5 files
            entry_lines.append(f"- {file}")
        if len(modified_files) > 5:
            entry_lines.append(f"- ... and {len(modified_files) - 5} more files")
        entry_lines.append("")

    entry_lines.extend([
        "**Next Actions:**",
        "- [ ] [To be filled in if needed]",
        "",
        "---",
        ""
    ])

    return "\n".join(entry_lines)


def main():
    """Update session state file on session end."""
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Get or create session file
        session_file, session_number, is_new = get_or_create_session_file()

        # Create session entry
        entry = create_session_entry(session_number, data)

        # Append to session file
        with open(session_file, 'a', encoding='utf-8') as f:
            f.write(entry)

        # Output confirmation
        status = "created" if is_new else "updated"
        output = f"""<system-reminder>
✅ Session state {status}: {session_file.name}
Session {session_number} logged

Note: Fill in session details manually in {session_file}
</system-reminder>"""

        print(output)
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON from stdin: {e}", file=sys.stderr)
        # Don't fail session on JSON error
        sys.exit(0)
    except Exception as e:
        print(f"ERROR in update-session-state: {e}", file=sys.stderr)
        # Don't fail session on error
        sys.exit(0)


if __name__ == "__main__":
    main()
