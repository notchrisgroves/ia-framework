---
name: framework-update
description: Update the IA Framework while preserving your customizations
---

# /framework-update - Safe Framework Updates

You are helping the user safely update their IA Framework installation while preserving their customizations.

## Overview

The user has customized their framework (added skills, modified agents, created commands, changed settings). They want to pull updates from the upstream IA Framework repository without losing their work.

## Your Task

Execute this workflow step by step:

---

## Phase 1: Fetch Upstream

1. **Check git status**: Verify this is a git repository

```bash
# Check if we're in a git repo
git rev-parse --git-dir 2>/dev/null || echo "NOT A GIT REPO"
```

2. **Setup upstream remote**: Ensure upstream points to the public IA Framework

```bash
# Check/add upstream remote
git remote get-url upstream 2>/dev/null || git remote add upstream https://github.com/notchrisgroves/ia-framework.git

# Fetch latest from upstream (doesn't modify working directory)
git fetch upstream main
```

3. **Create staging directory**: Export upstream's .claude to staging

```bash
# Create clean staging directory
rm -rf .ia-staging
mkdir -p .ia-staging

# Export upstream's .claude directory to staging (clean, no .git)
git archive upstream/main -- .claude | tar -x -C .ia-staging --strip-components=1
```

4. **Record version info**:

```bash
upstream_commit=$(git rev-parse upstream/main)
upstream_date=$(git log -1 --format=%ci upstream/main)
local_commit=$(git rev-parse HEAD)
echo "Upstream: $upstream_commit ($upstream_date)"
echo "Local: $local_commit"
```

---

## Phase 2: Analyze Differences

Compare the staging directory (`.ia-staging/`) against the user's active directory.

For each file category:

**Settings (`settings.json`)**:
- Identify new keys added upstream
- Identify keys the user has customized
- Plan a smart merge that adds new keys while preserving user values

**Skills (`skills/`)**:
- New skills in upstream → Available to add
- Modified skills → Compare if user has customized
- User's custom skills (not in upstream) → Never touch

**Agents (`agents/`)**:
- New agents available
- Modified agents (usually safe to update)
- User's custom agents → Preserve

**Commands (`commands/`)**:
- New commands from upstream
- Don't overwrite user's custom commands
- Identify conflicts where both changed

**Hooks (`hooks/`)**:
- Critical: hooks often contain custom logic
- Check if user has modified vs. upstream version
- Identify breaking changes

**Library/Docs/Tools**:
- Usually safe to update
- Check for user modifications

---

## Phase 3: Generate Report

Present a clear, organized report:

```
╔════════════════════════════════════════════════════════════════════╗
║                    IA FRAMEWORK UPDATE AVAILABLE                   ║
║                    Upstream: [commit hash]                         ║
║                    Your version: [commit hash]                     ║
╠════════════════════════════════════════════════════════════════════╣
║ SUMMARY                                                            ║
║ • X new files available                                            ║
║ • Y files updated upstream                                         ║
║ • Z potential conflicts with your customizations                   ║
╚════════════════════════════════════════════════════════════════════╝
```

Then organize by category:

**🔴 REQUIRES ATTENTION** (conflicts with your customizations)
- List files where both upstream changed AND user modified
- Show what would be lost if blindly updated
- Recommend merge strategy

**🟢 SAFE TO AUTO-UPDATE** (you haven't modified these)
- List files that can be updated without risk
- These match your current upstream version

**🆕 NEW FEATURES** (available to add)
- New skills, agents, commands
- Brief description of what each does

**📝 YOUR CUSTOMIZATIONS** (will be preserved)
- List user's custom files that don't exist upstream
- Confirm these are safe

---

## Phase 4: Get User Decision

Present clear options:

```
What would you like to do?

[A] Apply all safe updates + add all new features (recommended)
[S] Step through each change individually
[C] Conservative - only safe updates, skip new features
[M] Manual - show me the diffs, I'll decide everything
[N] Not now - keep staging for later review
```

---

## Phase 5: Execute Updates

For approved changes:

1. **Create backup**:

```bash
timestamp=$(date +%Y%m%d_%H%M%S)
mkdir -p .ia-backups/$timestamp
# Backup files that will be modified
cp -r skills .ia-backups/$timestamp/
cp -r agents .ia-backups/$timestamp/
cp -r commands .ia-backups/$timestamp/
cp settings.json .ia-backups/$timestamp/
```

2. **Apply changes**:
   - Copy approved new files from staging
   - For settings.json: perform intelligent merge (preserve user keys, add new ones)
   - For conflicts user approved: apply the merge strategy they chose

3. **Update tracking**:

```bash
echo "$(date -Iseconds) $(git rev-parse upstream/main)" >> .ia-sync-history
```

---

## Phase 6: Validate

After applying updates:
1. Check that settings.json is valid JSON
2. Verify no syntax errors in key files
3. Report success or any issues

---

## Phase 7: Cleanup

Ask if user wants to:
- Keep `.ia-staging/` for reference
- Remove it to save space (recommended)

```bash
rm -rf .ia-staging
```

---

## Important Notes

- **Never overwrite without asking** when user has customized a file
- **Always backup** before modifying existing files
- **Preserve user identity**: Custom skills, agents, settings
- **Be conservative**: When in doubt, ask rather than overwrite
- **Explain clearly**: Users should understand what each change does

## Handling Edge Cases

**First time running `/framework-update`**:
- No sync history exists
- Treat all current files as "user's version" (may be customized)
- Be extra careful, ask more questions

**User has diverged significantly**:
- Many files modified
- Recommend reviewing section by section
- Offer to show detailed diffs

**Not a git repo (downloaded as ZIP)**:
- Inform user they should clone properly for easier updates
- Offer manual comparison guidance

---

## Begin Now

Start by checking the git status and fetching upstream. Then analyze and report.
