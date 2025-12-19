#!/usr/bin/env python3
"""
Level 0 Hook: Auto-load framework context on session start

Trigger: SessionStart (every new conversation)
Purpose: Load CLAUDE.md for framework navigation
Output: CLAUDE.md wrapped in <system-reminder> tags
"""
import json
import sys
import io
from pathlib import Path

# Ensure stdout uses UTF-8 encoding (Windows fix)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    """Load and inject CLAUDE.md into conversation on session start."""
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Load CLAUDE.md from framework root
        claude_md = Path('CLAUDE.md')
        if not claude_md.exists():
            print("WARNING: CLAUDE.md not found in framework root", file=sys.stderr)
            sys.exit(1)

        # Read file contents with UTF-8 encoding
        content = claude_md.read_text(encoding='utf-8')

        # Inject into conversation as system reminder
        print(f"<system-reminder>\n{content}\n</system-reminder>")
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR in load-framework-context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
