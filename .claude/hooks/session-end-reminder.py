#!/usr/bin/env python3
"""
Session End Hook - Automatic Session State Reminder

Fires on SessionEnd event to remind about saving session state
for multi-session projects.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def find_recent_session_file():
    """Check if there's a session file for today."""
    sessions_dir = Path("sessions")
    if not sessions_dir.exists():
        return None

    today = datetime.now().strftime("%Y-%m-%d")

    # Look for today's session files
    session_files = list(sessions_dir.glob(f"{today}-*.md"))

    if session_files:
        return session_files[0]  # Return most recent

    return None

def check_if_multi_session_work():
    """
    Heuristics to detect if this was multi-session work:
    - Session file exists for today
    - Work lasted >1 hour (not implemented - would need session start time)
    - Multiple git commits today
    """
    # Check for session file
    session_file = find_recent_session_file()

    return session_file is not None, session_file

def main():
    """
    SessionEnd hook - remind to save session state.
    """

    is_multi_session, session_file = check_if_multi_session_work()

    if is_multi_session:
        print("\n" + "="*70)
        print("SESSION END REMINDER")
        print("="*70)
        print(f"\n[OK] Active session file detected: {session_file}")
        print("\n[!] BEFORE CLOSING:")
        print("   1. Update session file with:")
        print("      - Work completed this session")
        print("      - Current state/status")
        print("      - Next steps/priorities")
        print("      - Any blockers or decisions needed")
        print("\n   2. Format: See library/templates/SESSION-STATE-TEMPLATE.md")
        print("\n   3. Quick update command:")
        print(f"      # Add session notes to {session_file}")
        print("\n" + "="*70 + "\n")
    else:
        # Check if this SHOULD have been a multi-session project
        print("\n" + "="*70)
        print("SESSION END")
        print("="*70)
        print("\n[i] No active session file detected.")
        print("\n   If this was complex work that may continue:")
        print("   > Create session file: sessions/YYYY-MM-DD-project-name.md")
        print("   > Template: library/templates/SESSION-STATE-TEMPLATE.md")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
