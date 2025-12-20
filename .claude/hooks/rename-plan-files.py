#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plan File Naming Hook

Triggers after Write tool creates a file in the plans/ directory.
Prompts user for a descriptive name and renames the file.

Hook Type: PostToolUse (Write tool)
Matcher: plans/*.md

Author: IA Framework
Created: 2025-12-19
"""

import json
import os
import re
import sys
from pathlib import Path


def main():
    """Check if a plan file was just created and prompt for rename."""

    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    # Get tool info
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only trigger for Write tool
    if tool_name != "Write":
        return

    # Get the file path that was written
    file_path = tool_input.get("file_path", "")

    # Only trigger for files in plans/ directory
    if "/plans/" not in file_path and "\\plans\\" not in file_path:
        return

    # Only trigger for .md files
    if not file_path.endswith(".md"):
        return

    # Check if the filename looks auto-generated (adjective-noun-noun pattern)
    filename = Path(file_path).stem

    # Pattern for random names like "optimized-jumping-whistle"
    random_pattern = re.compile(r'^[a-z]+-[a-z]+-[a-z]+$')

    if not random_pattern.match(filename):
        # Already has a descriptive name
        return

    # Output message to prompt user
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Plan File Created: {filename}.md

This plan has an auto-generated name. Consider renaming it:

  mv "{file_path}" "plans/YOUR-DESCRIPTIVE-NAME.md"

Example names:
  - auth-system-refactor.md
  - api-migration-plan.md
  - security-audit-findings.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    main()
