---
type: documentation
title: Hierarchical Context Loading Architecture
classification: public
version: 3.0
last_updated: 2025-12-11
---

# Hierarchical Context Loading Architecture

**Version:** 3.0 (Updated for universal framework)
**Date:** 2025-12-11
**Status:** Production

---

## Overview

This document describes the hierarchical context loading system that prevents CLAUDE.md bloat and ensures proper separation of concerns across organization, skill, and agent levels.

## Problem Statement

### Before (Monolithic CLAUDE.md)
- ❌ Root CLAUDE.md was 800+ lines
- ❌ Contained agent methodologies, tool lists, workflows
- ❌ Loaded entire system context for every session (wasteful)
- ❌ Hard to maintain (massive file edits)
- ❌ Agents duplicated information
- ❌ Low signal-to-noise ratio

### After (Hierarchical Loading)
- ✅ Root CLAUDE.md is navigation layer only (<250 lines)
- ✅ Skill-specific context in `skills/*/SKILL.md` (<500 lines each)
- ✅ Agent prompts are compact (<150 lines)
- ✅ On-demand loading (only load what's needed)
- ✅ Easy maintenance (update one file)
- ✅ High signal-to-noise ratio

## Architecture Layers

### Layer 1: Organization (Root CLAUDE.md)

**File:** `CLAUDE.md` (framework root)
**Size Limit:** 250 lines
**Purpose:** Navigation layer + critical systems

**Contains:**
- System architecture overview
- Agent registry (pointers to agents/)
- Skill directory (pointers to skills/)
- Global stack preferences (Python, Bash, bun, uv)
- Tool selection priority (high-level)
- Security testing protocol (high-level)

**FORBIDDEN Content:**
- Agent workflows
- Skill methodologies
- Detailed tool lists
- Engagement templates
- Reporting standards

**Update When:**
- New agent created
- New skill added
- Global preference changes
- Architecture changes

---

### Layer 2: Skill Context

**Files:** `skills/[skill-name]/SKILL.md`
**Size Limit:** 500 lines per file
**Purpose:** Complete skill-specific context with progressive loading

**Contains:**
- Quick start (high-level overview)
- Critical rules summary (3-5 non-negotiable rules)
- Workflows and methodologies (navigation to extracted files)
- Tool lists (framework tools, skill tools, commands)
- Default configurations (headers, settings)
- Template references (not full templates)
- Output directory mappings
- Reporting standards

**Progressive Loading Pattern:** SKILL.md acts as navigation layer, detailed content extracted to:
- `methodologies/` - Complete process documentation
- `reference/` - Standards, frameworks, mappings
- `workflows/` - Step-by-step procedures
- `templates/` - Template files

**Example Skills:**
- `skills/security-testing/SKILL.md` - Pentest, vuln-scan, segmentation
- `skills/writer/SKILL.md` - Blog posts, technical docs
- `skills/osint-research/SKILL.md` - Intelligence gathering
- `skills/career/SKILL.md` - Career, coaching, mentorship
- `skills/legal/SKILL.md` - Legal compliance with citations

**Update When:**
- Skill workflow changes
- New tools added to skill
- Template standards updated
- Methodology refined
- Extracted content files updated

---

### Layer 3: Agent Prompts

**Files:** `agents/[agent-name].md`
**Size Limit:** 150 lines per file
**Purpose:** Agent identity and context loading instructions

**Contains:**
- Agent role definition
- Skill SKILL.md reference (pointer)
- Specialized behavior instructions
- Context loading order (mandatory)
- Communication style

**Example Structure:**

```markdown
---
name: security
description: Professional security agent
model: sonnet
---

# MANDATORY FIRST ACTION

**LOAD CONTEXT IN THIS ORDER:**

1. Read CLAUDE.md (bootloader)
2. Read skills/[detected-skill]/SKILL.md (skill context)
3. Read sessions/YYYY-MM-DD-project.md (if exists)

## Core Identity
[Agent role and philosophy]

## Workflow Execution
[Workflow reference - details in skills/*/SKILL.md]

## Tool Usage Priority
[Tool priority - details in skills/*/SKILL.md]

## Communication Style
[Output format]
```

**Update When:**
- Agent behavior changes
- Context loading order changes
- New specialized instructions needed

---

## Context Loading Flow

### User Invokes Agent

```
User: "Start pentest for Acme Corp"
       ↓
Claude Code invokes security agent
       ↓
Agent startup: Load context files
       ↓
1. Read CLAUDE.md
   - System architecture
   - Global preferences
   - Tool selection priority
       ↓
2. Read skills/security-testing/SKILL.md
   - Workflow phases
   - Testing methodologies
   - Tool catalog
   - Reporting standards
       ↓
3. Read sessions/2025-12-11-acme-pentest.md (if exists)
   - Previous session context
   - Decisions made
   - Files created
       ↓
Agent ready: Execute workflow
```

### Benefits
- **Token Efficient:** Load only what's needed
- **Fast Startup:** Smaller files load faster
- **Contextual:** Agent gets exact context required
- **Maintainable:** Update one file vs monolithic CLAUDE.md

---

## Agent-to-Skill Mapping

| Agent | Skills (Auto-Detected) | SKILL.md Locations |
|-------|------------------------|-------------------|
| **security** | Security operations | `skills/security-testing/`, others as needed |
| **writer** | Content creation | `skills/writer/`, `skills/osint-research/` (for research) |
| **advisor** | Personal development, research, QA | `skills/career/`, `skills/osint-research/`, `skills/qa-review/` |
| **legal** | Legal compliance | `skills/legal/` |

---

## File Size Limits Summary

| Level | File | Size Limit | Purpose |
|-------|------|------------|---------|
| Org | `CLAUDE.md` | 250 lines | Navigation + critical systems |
| Skill | `skills/*/SKILL.md` | 500 lines | Full skill context with progressive loading |
| Agent | `agents/*.md` | 150 lines | Agent prompt (compact) |

**Note:** Current NEW framework targets these limits from the start (not aspirational).

---

## Routing Decision Tree

### User Request: "Update CLAUDE.md with..."

**STEP 1: Identify Context Level**

```
What is being updated?
│
├─ "Add new agent to system"
│  → UPDATE: Root CLAUDE.md (agents/ registry)
│
├─ "Update pentest methodology"
│  → UPDATE: skills/security-testing/SKILL.md
│
├─ "Add new tool to workflow"
│  → UPDATE: skills/[skill]/SKILL.md (tools section)
│
├─ "Change default testing headers"
│  → UPDATE: skills/security-testing/SKILL.md (config section)
│
├─ "Add new global stack preference"
│  → UPDATE: Root CLAUDE.md (stack preferences)
│
└─ "Update agent behavior"
   → UPDATE: agents/[agent].md
```

**STEP 2: Ask Clarifying Question**

Before updating ANY CLAUDE.md:

```
"I need to confirm the update location:

- Root CLAUDE.md (org-level navigation)?
- skills/[skill]/SKILL.md (skill-specific context)?
- agents/[agent].md (agent prompt)?

Based on your request, I believe this should go in: [TARGET]

Is this correct?"
```

**STEP 3: Execute Update**

Only after confirmation and validation.

---

## Success Metrics

### Token Efficiency
- **Before:** 800-line CLAUDE.md loaded every session
- **After:** 250-line nav + 500-line skill = 750 lines (6% reduction, but better organized)
- **For simple tasks:** Only 250-line nav loaded (69% reduction)

### Maintainability
- **Before:** Update 1 file (800 lines) → hard to find sections
- **After:** Update specific file (150-500 lines) → easy to locate

### Discoverability
- **Before:** Ctrl+F in massive file
- **After:** Navigate hierarchy (root → skill → agent)

---

## Forbidden Operations

**❌ NEVER add to root CLAUDE.md:**
- Agent descriptions (use agents/*.md)
- Skill workflows (use skills/*/SKILL.md)
- Detailed tool lists (skill-specific)
- Engagement data (belongs in output/engagements/)
- Detailed configs (use docs/)
- Infrastructure details (use skills/infrastructure-ops/)

**Root CLAUDE.md = Navigation layer only**

---

## Related Documentation

- **Agent Files:** `agents/security.md`, `agents/writer.md`, `agents/advisor.md`, `agents/legal.md`
- **Skill Files:** `skills/*/SKILL.md`
- **FILE-LOCATION-STANDARDS.md:** Where files belong
- **session-checkpoint-enforcement.md:** Multi-session protocol

---

**Version:** 3.0 (Universal framework design)
**Last Updated:** 2025-12-11
**Framework:** Intelligence Adjacent (IA)
