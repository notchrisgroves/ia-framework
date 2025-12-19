# IA Framework Installation Guide

## Critical: Installation Location

**The IA Framework MUST be installed at `~/.claude`** (or `%USERPROFILE%\.claude` on Windows)

This is **required** because:
- Claude Code automatically loads `CLAUDE.md` from this location
- Settings in `settings.json` are read from `~/.claude/`
- Commands in `commands/` are discovered relative to this path
- All framework paths assume this root directory

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Claude Code CLI | Latest | https://claude.com/claude-code |
| Python | 3.10+ | For validation tools |
| Git | 2.x+ | For version control |

---

## Installation Steps

### 1. Clone to Correct Location

**Linux/macOS:**
```bash
git clone <your-repo-url> ~/.claude
cd ~/.claude
```

**Windows (PowerShell):**
```powershell
git clone <your-repo-url> $env:USERPROFILE\.claude
cd $env:USERPROFILE\.claude
```

**Windows (Command Prompt):**
```cmd
git clone <your-repo-url> %USERPROFILE%\.claude
cd %USERPROFILE%\.claude
```

### 2. Configure Credentials

```bash
cp .env.template .env
# Edit .env and replace REPLACE_WITH_YOUR_* placeholders with actual API keys
```

**Required credentials:**
- `ANTHROPIC_API_KEY` - For Claude API access
- `OPENROUTER_API_KEY` - For multi-model routing (optional)
- `XAI_API_KEY` - For Grok models (optional)

See `docs/CREDENTIAL-HANDLING-ENFORCEMENT.md` for security standards.

### 3. Verify Installation

```bash
# Launch Claude Code from any directory
claude-code

# Verify framework loaded
# You should see CLAUDE.md context in the conversation

# Check available commands
ls ~/.claude/commands/
```

---

## Post-Installation Verification

Run the framework health check:

```bash
python ~/.claude/tools/validation/framework-health-check.py
```

This validates:
- Required directories exist
- CLAUDE.md is properly formatted
- Agent files are within line limits
- Credential templates are in place

---

## Common Issues

### Framework Not Loading

**Symptom:** Claude Code doesn't show CLAUDE.md context

**Solution:** Verify installation location:
```bash
ls ~/.claude/CLAUDE.md  # Should exist
```

### Commands Not Found

**Symptom:** Slash commands like `/pentest` don't work

**Solution:** Ensure you're in the correct directory or that `~/.claude/commands/` exists

### Credential Errors

**Symptom:** Scripts fail with "API key not found"

**Solution:** Check `.env` file:
```bash
cat ~/.claude/.env | grep -v "^#"  # Should show key=value pairs
```

---

## Updating the Framework

```bash
cd ~/.claude
git pull origin main
```

---

## Uninstallation

```bash
rm -rf ~/.claude
```

**Note:** This removes all framework files including any custom configurations.

---

**Version:** 4.0
**Last Updated:** 2025-12-17
