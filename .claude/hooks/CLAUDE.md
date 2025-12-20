# Hooks - Event-Driven Framework Automation

> **Note:** This is a manual reference file for the hooks/ subsystem. It is NOT auto-loaded by hooks. Only root CLAUDE.md is auto-loaded on session start.

**Purpose:** Event handlers that execute during Claude Code lifecycle events

---

## Hook Architecture

**Available hooks:**

| Hook | Event | Purpose |
|------|-------|---------|
| load-framework-context.py | SessionStart | Loads CLAUDE.md on session start |
| load-agent-skill-context.py | PreToolUse:Task | Injects agent/skill context for Task tool |
| detect-commands.py | UserPromptSubmit | Suggests slash commands based on keywords |
| session-end-reminder.py | SessionEnd | Reminds to save session state |
| enforce-session-boundary.py | PreToolUse | Prevents cross-session file access |
| rename-plan-files.py | PostToolUse | Auto-renames plan files |
| update-session-state.py | PostToolUse | Updates session tracking |
| rebuild-tool-registry.py | PostToolUse | Rebuilds tool registry on changes |
| validate-tool-structure.py | PreToolUse | Validates tool structure |

**Pre-commit hooks:** `hooks/pre-commit/*.sh` - Git validation before commits

---

## How Hooks Work

**1. Configuration:** Hooks are configured in `settings.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {"command": "python hooks/load-framework-context.py"}
    ],
    "PreToolUse": [
      {"matcher": {"tool_name": "Task"}, "command": "..."}
    ]
  }
}
```

**2. Execution:** Claude Code triggers hooks at lifecycle events
**3. Output:** Hook output appears in conversation as `<system-reminder>`

---

## Core Hooks Explained

### load-framework-context.py
**Event:** SessionStart
**Purpose:** Ensures CLAUDE.md is loaded at session start

```python
# Outputs CLAUDE.md content as system reminder
# Provides framework navigation on every session
```

### load-agent-skill-context.py
**Event:** PreToolUse (Task tool)
**Purpose:** Injects appropriate agent + skill context when Task tool is invoked

```python
# Detects: Task(subagent_type="security")
# Loads: agents/security.md + skills/security-testing/SKILL.md
# Injects as: <system-reminder> for the spawned agent
```

This is the core of the hierarchical context loading system.

### detect-commands.py
**Event:** UserPromptSubmit
**Purpose:** Suggests slash commands when keywords are detected

```python
# User types: "I need to analyze a job posting"
# Hook suggests: "Consider using /job-analysis"
```

Keyword mappings in `KEYWORD_MAP` dict.

### session-end-reminder.py
**Event:** SessionEnd
**Purpose:** Reminds to update session state before closing

```python
# Checks if session file exists for today
# Reminds to save state if multi-session project
```

### enforce-session-boundary.py
**Event:** PreToolUse (Read/Edit)
**Purpose:** Prevents accessing files from other sessions

```python
# Blocks: Reading session files not matching current session
# Allows: Current session files, non-session files
```

---

## Pre-Commit Hooks

Located in `hooks/pre-commit/`, these run before git commits:

| Hook | Purpose |
|------|---------|
| validate-documentation.sh | Validates against 7 constitutional rules |
| validate-blog-structure.sh | Ensures blog posts have correct structure |
| validate-support-skills.sh | Validates support skill patterns |
| prevent-hardcoded-counts.sh | Blocks hardcoded counts in docs |
| block-infrastructure-leaks.sh | Prevents credential leaks |
| enforce-output-directory.sh | Enforces file location standards |
| prevent-duplicate-tracking.sh | Prevents duplicate file tracking |
| readme-validation.sh | README format validation |

**Bypass (NOT recommended):** `git commit --no-verify`

---

## Creating New Hooks

**1. Create Python script in `hooks/`:**
```python
#!/usr/bin/env python3
"""Hook description."""
import json
import sys

def main():
    # Read hook input from stdin (if applicable)
    # Perform hook logic
    # Output to stdout (becomes system-reminder)
    print("Hook message to inject")

if __name__ == "__main__":
    main()
```

**2. Register in `settings.json`:**
```json
{
  "hooks": {
    "EventName": [
      {"command": "python hooks/your-hook.py"}
    ]
  }
}
```

**3. Test:** Trigger the event and verify hook executes

---

## Hook Events Reference

| Event | Trigger | Use Case |
|-------|---------|----------|
| SessionStart | New session begins | Load context, set state |
| SessionStart:clear | After /clear command | Reset context |
| SessionEnd | Session closes | Save state, cleanup |
| PreToolUse | Before any tool | Validation, injection |
| PostToolUse | After any tool | Logging, updates |
| UserPromptSubmit | User sends message | Suggestions, routing |

**Matchers:** Filter by tool name, file path, etc.
```json
{"matcher": {"tool_name": "Task"}, "command": "..."}
{"matcher": {"tool_name": "Read", "file_path": "*.md"}, "command": "..."}
```

---

## Files in This Directory

```
hooks/
├── CLAUDE.md                    (This file - hooks system overview)
├── README.md                    (Quick reference)
├── load-framework-context.py    (SessionStart - loads CLAUDE.md)
├── load-agent-skill-context.py  (PreToolUse - agent/skill injection)
├── detect-commands.py           (UserPromptSubmit - command suggestions)
├── session-end-reminder.py      (SessionEnd - state reminder)
├── enforce-session-boundary.py  (PreToolUse - session isolation)
├── rename-plan-files.py         (PostToolUse - plan file naming)
├── update-session-state.py      (PostToolUse - session tracking)
├── rebuild-tool-registry.py     (PostToolUse - registry updates)
├── validate-tool-structure.py   (PreToolUse - tool validation)
├── test_hooks.py                (Hook testing utilities)
├── pre-commit/                  (Git pre-commit hooks)
│   ├── validate-documentation.sh
│   ├── validate-blog-structure.sh
│   ├── validate-support-skills.sh
│   └── ... (see pre-commit/ for full list)
└── startup/                     (Startup scripts)
```

---

## Testing Hooks

**Manual test:**
```bash
# Test hook directly
python hooks/detect-commands.py < test_input.json

# Test pre-commit hooks
./hooks/pre-commit/validate-documentation.sh
```

**Validation:**
```bash
python hooks/test_hooks.py
```

---

## Common Issues

**Hook not executing:**
- Check `settings.json` configuration
- Verify Python path is correct
- Check hook script is executable

**Wrong context loaded:**
- Check matcher patterns in settings.json
- Verify agent/skill routing in load-agent-skill-context.py

**Pre-commit blocking commits:**
- Run the specific hook manually to see detailed errors
- Fix violations before committing
- Use `--no-verify` only as last resort

---

## References

**Configuration:**
- `settings.json` - Hook registration
- `.claude/settings.local.json` - Local overrides (gitignored)

**Documentation:**
- `docs/hierarchical-context-loading.md` - Context loading system
- `docs/session-checkpoint-enforcement.md` - Session boundaries
- [Claude Code Hooks Guide](https://docs.anthropic.com/en/docs/claude-code/hooks)

---

**Hooks:** Event-driven automation for framework behavior
**Location:** `hooks/` directory
**Framework:** Intelligence Adjacent (IA) v1.0.0
