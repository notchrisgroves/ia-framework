---
type: documentation
title: Session Checkpoint Enforcement Protocol
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Session Checkpoint Enforcement Protocol - MANDATORY

**Status:** 🚨 CRITICAL SYSTEM ARCHITECTURE - STRICT ENFORCEMENT REQUIRED
**Date:** 2025-11-13
**Priority:** P0 - Framework Foundation

---

## The Problem (Context Drift)

**Long sessions without checkpoints = architectural failure:**
- Decisions forgotten between sessions
- Files created in random locations
- Context window fills, critical info lost
- Users repeat same questions
- Agents re-analyze same problems
- Work gets duplicated or contradicts previous decisions

**Symptom:** "Wait, didn't we already decide this?" or "Where did we save that?"

---

## The Solution (Mandatory Checkpointing)

**SESSION-STATE.md files at predefined locations** - Not optional, not suggested, **REQUIRED**.

### Core Principle

**Every multi-session project MUST have a SESSION-STATE.md file that:**
1. Records decisions made
2. Tracks files created/modified
3. Lists next actions
4. Maintains last 3 session summaries (prevents balloon)
5. Serves as context reload point

---

## Enforcement Rules (MANDATORY)

### Rule 1: Project Detection

**ALL agents MUST detect if working on multi-session project:**

**Project types requiring session files:**
- Penetration tests (output/engagements/pentest/*)
- Vulnerability scans (output/engagements/vuln-scan/*)
- Risk assessments (output/engagements/risk-assessment/*)
- Blog posts (blog/*)
- Infrastructure work (skills/infrastructure-ops/)
- Any engagement spanning 3+ sessions

**Detection trigger:** If project directory exists OR 3+ related tool calls made, checkpoint required.

### Rule 2: Checkpoint Triggers (Automatic)

**Agents MUST checkpoint at these points:**

1. **Task completion** - After completing significant task (pentest phase, blog draft, config change)
2. **Context switch** - Before switching between projects (pentest → blog → advisory)
3. **Session end** - Before conversation summary (if multi-session project active)
4. **File creation** - After creating 5+ files in same project
5. **Decision made** - After architectural/strategic decision
6. **User requests checkpoint** - `/checkpoint` command (always honor)

**No exceptions. No "I'll do it later." Do it NOW.**

### Rule 3: Location Standards (SIMPLIFIED)

**ALL SESSION-STATE files go to ONE location:**

```
sessions/YYYY-MM-DD-project-name.md
```

**That's it. Single flat directory. No subfolders. No guessing.**

**Examples:**
- `sessions/2025-12-03-blog-ia-intro.md`
- `sessions/2025-12-03-pentest-acmecorp.md`
- `sessions/2025-12-03-hook-cleanup.md`
- `sessions/2025-12-01-resources-reorganization.md`

**Benefits:**
- ✅ Agents ALWAYS know where to look (no "which folder?" problem)
- ✅ Date-sorted automatically by filename
- ✅ Easy to find: `ls sessions/ | grep "blog"`
- ✅ Easy to clean up old sessions
- ✅ Simple, predictable, maintainable

**NO exceptions. ONE location for ALL sessions.**

### Rule 4: Content Requirements (Mandatory Fields)

**Every session file MUST contain:**

```markdown
# Session State - [Project Name]

**Last Updated:** [ISO timestamp]
**Session Count:** [number]
**Status:** [active/paused/complete]
**Agent:** [security/writer/advisor/legal]

---

## Current Context (Last 3 Sessions)

### Session [N] - [YYYY-MM-DD HH:MM]
**Tasks Completed:**
- [x] Task 1
- [x] Task 2

**Decisions Made:**
- Decision 1: [rationale]
- Decision 2: [rationale]

**Files Created/Modified:**
- path/to/file1.md
- path/to/file2.md

**Next Actions:**
- [ ] Next task 1
- [ ] Next task 2

---

## Key Decisions Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| YYYY-MM-DD | [decision] | [why] | [what changed] |

---

## Active Files

**Primary Deliverable:** [path to main file]
**Supporting Docs:** [list of paths]

---

## Blockers & Open Questions

- [ ] [Blocker 1]
- [ ] [Question for user]

---

## Metrics

- Total Sessions: [count]
- Files Created: [count]
- Completion: [% if applicable]
```

**Missing any section = incomplete checkpoint = violation.**

### Rule 5: Context Reload (Mandatory Start)

**When resuming multi-session project:**

**Step 1:** Check `sessions/` for project files: `ls sessions/ | grep "project-name"`
**Step 2:** If exists, READ IT FIRST before doing anything else
**Step 3:** Load "Active Files" into context
**Step 4:** Review "Key Decisions Log"
**Step 5:** Check "Next Actions"
**Step 6:** Resume work with full context

**If SESSION-STATE.md doesn't exist but should = create it in `sessions/YYYY-MM-DD-project-name.md` immediately.**

### Rule 6: File Location Validation (Session End)

**Before ending ANY multi-session project:**

**Agents MUST check scratchpad/ for misplaced permanent documentation:**

**Step 1:** Scan scratchpad/ for files created during session
**Step 2:** Classify each file (permanent vs temporary)
**Step 3:** If permanent docs found in scratchpad/ → WARN USER
**Step 4:** Suggest correct location for each file
**Step 5:** Wait for user to move files OR confirm they're temporary

**Classification check:**
- Gap analysis, audits, roadmaps → docs/[project]/
- Blog content → blog/YYYY-MM-DD-title/
- Engagement docs → output/engagements/[type]/[id]/
- Session state → sessions/YYYY-MM-DD-project-name.md
- Architecture/standards → docs/[category]/

**See:** `docs/FILE-LOCATION-STANDARDS.md` for classification rules

**No exceptions. Scratchpad cleanup is MANDATORY before session end.**

---

## Success Metrics

**Checkpoint system working when:**
- ✅ Users can resume projects without re-explaining context
- ✅ Agents reload context from session file, not user messages
- ✅ No repeated discussions about same decisions
- ✅ All project files in predictable locations
- ✅ Session-to-session continuity maintained
- ✅ Zero "where did we save that?" questions

---

## Template (Copy-Paste Ready)

**File:** `library/templates/SESSION-STATE-TEMPLATE.md`

```markdown
# Session State - [Project Name]

**Last Updated:** [YYYY-MM-DD HH:MM:SS]
**Session Count:** 1
**Status:** active
**Agent:** [security/writer/advisor/legal]
**Project Type:** [pentest/blog/advisory/infrastructure]

---

## Current Context (Last 3 Sessions)

### Session 1 - [YYYY-MM-DD HH:MM]
**Tasks Completed:**
- [x] Initial setup
- [x] Context established

**Decisions Made:**
- Decision 1: [description] - Rationale: [why]

**Files Created/Modified:**
- path/to/file.md

**Next Actions:**
- [ ] Task 1
- [ ] Task 2

---

## Key Decisions Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| YYYY-MM-DD | [decision] | [why this choice] | [what it affects] |

---

## Active Files

**Primary Deliverable:** [path to main file]
**Supporting Docs:**
- path/to/doc1.md
- path/to/doc2.md

---

## Blockers & Open Questions

- [ ] Blocker or question 1
- [ ] Blocker or question 2

---

## Metrics

- Total Sessions: 1
- Files Created: 0
- Completion: 0%
- Last Checkpoint: [timestamp]

---

## Notes

[Any additional context or observations]
```

---

**Status:** 🚨 ENFORCEMENT ACTIVE - NO EXCEPTIONS
**Compliance:** MANDATORY for all agents on all multi-session projects
**Verification:** Every session end, every project resume

---

**Remember:** This isn't about bureaucracy. This is about **not wasting the user's time repeating context.** Checkpoint discipline = respect for user's time and cognitive load.
