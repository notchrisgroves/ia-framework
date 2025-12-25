#!/usr/bin/env python3
"""
UserPromptSubmit Hook: Suggest parallel task orchestration

Trigger: UserPromptSubmit (every user message)
Purpose: Detect multi-task patterns and suggest parallel execution
Output: Parallel orchestration suggestion wrapped in <system-reminder> tags

Detection patterns:
- Multiple verbs with "and" / "also" / "as well"
- List markers (1. 2. 3. or bullet points)
- Multiple independent requests in one prompt
"""
import json
import re
import sys
import io

# Ensure stdout uses UTF-8 encoding (Windows fix)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Sequential dependency keywords (do NOT parallelize)
SEQUENTIAL_KEYWORDS = [
    "then", "after that", "once done", "when finished",
    "first", "next", "finally", "before", "after"
]

# Multi-task detection patterns
MULTI_TASK_PATTERNS = [
    r'\band\s+also\b',           # "and also"
    r'\bas\s+well\s+as\b',       # "as well as"
    r'\bAND\b',                  # Emphatic AND
    r'^\s*\d+\.\s+',             # Numbered list
    r'^\s*[-*]\s+',              # Bullet list
    r'\bplus\b',                 # "plus"
    r'\badditionally\b',         # "additionally"
]


def has_sequential_dependency(prompt):
    """Check if prompt contains sequential dependency keywords."""
    prompt_lower = prompt.lower()
    return any(kw in prompt_lower for kw in SEQUENTIAL_KEYWORDS)


def count_tasks(prompt):
    """Estimate number of independent tasks in prompt."""
    task_count = 0

    # Check for numbered lists
    numbered = re.findall(r'^\s*\d+\.\s+', prompt, re.MULTILINE)
    if numbered:
        task_count = max(task_count, len(numbered))

    # Check for bullet lists
    bullets = re.findall(r'^\s*[-*]\s+', prompt, re.MULTILINE)
    if bullets:
        task_count = max(task_count, len(bullets))

    # Check for "and" conjunctions with action verbs
    and_count = len(re.findall(r'\b(and|AND)\b', prompt))
    if and_count >= 2:
        task_count = max(task_count, and_count + 1)

    return task_count


def main():
    """Detect multi-task patterns and suggest parallel orchestration."""
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        # Skip if prompt is too short
        if len(prompt) < 50:
            sys.exit(0)

        # Skip if sequential dependencies detected
        if has_sequential_dependency(prompt):
            sys.exit(0)

        # Count potential tasks
        task_count = count_tasks(prompt)

        # Also check for multi-task patterns
        has_pattern = any(re.search(p, prompt, re.IGNORECASE) for p in MULTI_TASK_PATTERNS)

        # Suggest parallelization if 3+ tasks or strong pattern match
        if task_count >= 3 or (task_count >= 2 and has_pattern):
            output = f"""<system-reminder>
Parallel orchestration opportunity detected ({task_count} potential tasks).

Consider spawning background subagents for independent tasks:
- Use Task(run_in_background=true) for parallelizable work
- See CLAUDE.md "Parallel Task Orchestration" section
- Each subagent writes to sessions/parallel-{{id}}-task-N.md
</system-reminder>"""
            print(output)

        sys.exit(0)

    except Exception as e:
        # Fail gracefully - never block user prompt
        print(f"WARNING: Hook error in suggest-parallel-orchestration: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
