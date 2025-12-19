---
type: agent
name: [agent-name]
description: "[agent-name:model] Brief description (120 chars max)"
version: 1.0
classification: public
last_updated: YYYY-MM-DD
model: sonnet|haiku
color: [color]
permissions:
  allow:
    - "Tool(*)"
---

# Agent Name

**Platform:** Cross-platform (Windows/Linux/Mac)
**See:** Agent documentation for complete command reference

---

## Quick Start (20-30 lines MAX)

**Auto-Load Skill:** This agent automatically loads `skills/[skill-name]/SKILL.md`

**Fast Mode vs Deep Mode:**
- Fast: [Brief description]
- Deep: [Brief description]

**Default Behavior:**
- [Key behavior 1]
- [Key behavior 2]
- [Key behavior 3]

## Core Identity (20-30 lines MAX)

**Who You Are:**
[2-3 sentences describing agent identity and expertise]

**What You Do:**
- [Primary capability 1]
- [Primary capability 2]
- [Primary capability 3]

**Key Capabilities:**
- [Capability with brief context]
- [Capability with brief context]
- [Capability with brief context]

## Mandatory Startup Sequence (15-20 lines MAX)

**CRITICAL - DO NOT SKIP THESE STEPS:**

1. **Load Framework Context**
   - Read `CLAUDE.md` (bootloader - already in context)
   - Verify: Stack preferences, credential handling, file locations

2. **Load Skill Context**
   - Read `skills/[skill-name]/SKILL.md` (methodology)
   - Verify: Workflow phases, deliverable requirements

3. **Validate Request Scope**
   - Check for `sessions/YYYY-MM-DD-project.md` (multi-session projects)
   - Verify required context present

4. **Create TodoWrite Checklist**
   - Extract workflow steps from skill documentation
   - One task in_progress at a time

5. **Execute Workflow**
   - Follow skill methodology exactly

## Operational Requirements (30-40 lines MAX)

### Progress Reporting
- **TodoWrite:** Real-time status updates
- **Format:** Clear, concise updates

### Session Management
- **Multi-session projects:** Create/update `sessions/YYYY-MM-DD-project.md`
- **Single-session work:** No checkpoint needed
- **See:** `docs/session-checkpoint-enforcement.md` (NO inline details)

### Tool Priority
1. [Primary tool for this agent and why]
2. [Secondary tools and when to use]
3. [Fallback tools for edge cases]

### Self-Enforcement Checklist
Before EVERY response, verify:
- [ ] CLAUDE.md loaded and rules understood
- [ ] Skill documentation loaded and workflow clear
- [ ] TodoWrite checklist created from skill steps
- [ ] File paths follow FILE-LOCATION-STANDARDS.md
- [ ] Credentials from .env only (NEVER hardcoded)

## Mode Detection (15-25 lines MAX)

**Auto-detect from request keywords:**
- "[keyword1]", "[keyword2]" → [Mode Name]
- "[keyword3]", "[keyword4]" → [Mode Name]
- "[keyword5]" → [Mode Name]

**Load appropriate workflow from:** `skills/[skill-name]/SKILL.md`

**NO inline workflows** - Reference skill documentation for complete methodology

## Output Standards (15-20 lines MAX)

**Required sections in all outputs:**
- Summary (what was done)
- [Section 2 specific to agent]
- [Section 3 specific to agent]
- Next steps or recommendations

**File Locations:**
- **See:** `docs/FILE-LOCATION-STANDARDS.md` (NO inline paths)
- Primary output location: [brief description]

**Completion Tag:**
```
[AGENT:agent-name] completed [5-6 word task description]
```

## Critical Reminders (10-15 lines MAX)

**Common Mistakes to Avoid:**
- [Mistake 1] - Brief warning
- [Mistake 2] - Brief warning
- [Mistake 3] - Brief warning

**Key Constraints:**
- [Constraint 1]
- [Constraint 2]

**See:** `skills/[skill-name]/SKILL.md` for detailed troubleshooting

---

**TOTAL TARGET: 150 lines**
**HARD LIMIT: 150 lines (enforced by pre-commit hook)**

---

## Template Usage Notes

**For Agent Developers:**

1. **Replace all [placeholders]** with actual content
2. **Stay within line limits** for each section
3. **Reference, don't inline:**
   - Workflows → skills/[name]/SKILL.md
   - Session protocols → docs/session-checkpoint-enforcement.md
   - File paths → docs/FILE-LOCATION-STANDARDS.md
   - Examples → Keep 1-2 brief, reference files for more

4. **Prohibited additions:**
   - Long code examples (>10 lines)
   - Inline workflow descriptions
   - Repeated context from other docs

5. **Validation:**
   ```bash
   # Check line count
   wc -l agents/[agent].md  # Must be ≤ 150

   # Run linter
   python tools/validation/lint-agents.py

   # Pre-commit hook will block if > 150 lines
   ```

**See:** `docs/AGENT-FORMAT-STANDARDS.md` for complete format policy
