---
type: documentation
title: Agent Format Standards and Enforcement
classification: public
version: 1.0
last_updated: 2025-12-17
---

# Agent Format Standards

**Purpose:** Format requirements, validation, and editing guidelines for all agent files

**Enforcement:** Pre-commit hooks + manual validation

---

## Format Requirements

**All agents MUST follow these standards:**

### Line Limit (MANDATORY)
- **Maximum:** 150 lines per agent file
- **Recommended:** <140 lines (10-line buffer for future edits)
- **Enforcement:** Pre-commit hook blocks commits with agents >150 lines
- **Validation:** `python tools/validation/lint-agents.py`

### Structure (REQUIRED)
All agents must follow the structure from `library/templates/AGENT-TEMPLATE.md`:

1. **Quick Start** (20-30 lines)
   - Auto-load skills list
   - Request detection patterns
   - Brief overview

2. **Core Identity** (20-30 lines)
   - Who the agent is
   - What it does
   - Key capabilities

3. **Mandatory Startup Sequence** (15-20 lines)
   - Context loading steps
   - Tool catalog loading
   - Skill selection logic

4. **Operational Requirements** (30-40 lines)
   - Request type detection
   - Resource auto-detection
   - Session tracking protocol

5. **Output Standards** (15-20 lines)
   - Domain-specific standards
   - Quality requirements
   - Output locations

6. **Critical Reminders** (10-15 lines)
   - Key principles
   - Common pitfalls
   - Completion tag format

---

## Editing Guidelines

### When to Edit Agents

**✅ DO edit when:**
- Adding new routing keyword/pattern
- Fixing routing logic bug
- Updating agent identity/role
- Adding new skill integration

**❌ DON'T edit to:**
- Add workflow details (goes in skills/*/SKILL.md)
- Add examples (reference external files)
- Add reference materials (link to docs/)
- Inline templates (reference library/templates/)

### Before Editing ANY Agent

**MANDATORY Pre-Edit Checklist:**

1. **Read format guardian:**
   ```bash
   cat library/prompts/format-guardian.md
   ```
   This is your NON-NEGOTIABLE self-reminder of format rules.

2. **Check current line count:**
   ```bash
   wc -l agents/[agent-name].md
   ```
   **If >140 lines:** REMOVE content before adding new content.

3. **Run validation:**
   ```bash
   python tools/validation/lint-agents.py
   ```
   **Must pass** before making any changes.

4. **Reference instead of inline:**
   - Link to skills/*/SKILL.md for workflows
   - Link to docs/ for detailed documentation
   - Link to library/templates/ for templates

### If Agent Exceeds 150 Lines

**Step 1: Identify bloat**
- Look for inlined workflows → Extract to skills/*/workflows/
- Look for detailed procedures → Extract to skills/*/SKILL.md
- Look for examples → Extract to skills/*/templates/
- Look for reference materials → Extract to docs/

**Step 2: Extract and reference**
```markdown
# Before (inline)
## Workflow Details
[50 lines of detailed steps]

# After (reference)
## Workflow
See `skills/security-testing/workflows/pentest-init.md` for complete workflow.
```

**Step 3: Validate**
```bash
wc -l agents/[agent-name].md  # Must be ≤150
python tools/validation/lint-agents.py  # Must pass
```

---

## Content Restrictions

### ❌ NEVER Inline These

**Workflows:**
```markdown
# DON'T DO THIS:
## Pentest Workflow
Step 1: Scope definition
  - Define targets
  - Identify restrictions
  - Set timeline
Step 2: Reconnaissance
  [... 40 more lines ...]

# DO THIS INSTEAD:
## Workflow
See `skills/security-testing/workflows/pentest-init.md`
```

**Examples:**
```markdown
# DON'T DO THIS:
## Example: Job Analysis
User: "Analyze this job posting"
Agent: [detailed example with multiple steps]
[... 30 lines of example ...]

# DO THIS INSTEAD:
## Examples
See `skills/career/templates/job-analysis-example.md`
```

**Reference Materials:**
```markdown
# DON'T DO THIS:
## PTES Methodology
The Penetration Testing Execution Standard includes:
- Pre-engagement Interactions
- Intelligence Gathering
[... 50 lines of framework details ...]

# DO THIS INSTEAD:
## Methodology
Follows PTES standard. See `skills/security-testing/reference/ptes-framework.md`
```

---

## Validation

### Manual Validation

**Check line count:**
```bash
wc -l agents/*.md
```
**Expected output:**
```
136 agents/advisor.md    ✅ <150
147 agents/security.md   ✅ <150
115 agents/CLAUDE.md     ✅ <150
149 agents/legal.md      ✅ <150
150 agents/writer.md     ⚠️  At limit (optimize recommended)
```

**Run linter:**
```bash
python tools/validation/lint-agents.py
```

### Pre-Commit Validation

**Automatic enforcement:**
- Pre-commit hook scans all agents/*.md files
- Blocks commit if any agent >150 lines
- Provides error message with line count
- Must fix before commit allowed

**Hook location:** `hooks/pre-commit/validate-agent-format.py`

---

## Common Issues and Solutions

### Issue 1: Agent Keeps Growing Over Time

**Problem:** Small incremental edits push agent over 150 lines.

**Solution:**
- Set target at 140 lines (10-line buffer)
- Review and optimize every 5-10 edits
- Extract new content to appropriate locations

### Issue 2: Can't Find Where to Extract Content

**Decision tree:**

**Is it a workflow?**
→ Extract to `skills/*/workflows/[workflow-name].md`

**Is it a methodology/framework?**
→ Extract to `skills/*/reference/[framework-name].md`

**Is it an example?**
→ Extract to `skills/*/templates/[example-name].md`

**Is it detailed documentation?**
→ Extract to `docs/[topic].md`

**Is it a template?**
→ Already in `library/templates/` - just reference it

### Issue 3: Pre-Commit Hook Not Enforcing

**Check hook is installed:**
```bash
ls -la .git/hooks/pre-commit
```

**Verify hook executes:**
```bash
git commit --dry-run
```
Should see validation output.

**Manual enforcement:**
```bash
python hooks/pre-commit/validate-agent-format.py
```

---

## Comparison: Good vs Bad

### ❌ BAD: Bloated Agent (185 lines)

```markdown
# Security Agent

## Quick Start
[30 lines]

## Pentest Workflow
### Phase 1: Scope Definition
- Define targets in scope
- Identify out-of-scope items
- Set timeline and schedule
- Establish communication protocols
[... 50 more lines of detailed workflow ...]

### Phase 2: Reconnaissance
[... 40 more lines ...]

## PTES Methodology
The Penetration Testing Execution Standard...
[... 40 more lines of framework details ...]

## Examples
[... 25 more lines of examples ...]
```

### ✅ GOOD: Focused Agent (147 lines)

```markdown
# Security Agent

## Quick Start
[30 lines - same as before]

## Workflow Routing
- Pentest keywords → `skills/security-testing/workflows/pentest-init.md`
- Vuln scan keywords → `skills/security-testing/workflows/vuln-scan.md`
- Code review keywords → `skills/code-review/workflows/security-code-review.md`

## Methodology
Follows PTES, OWASP, NIST standards.
See `skills/security-testing/reference/` for complete frameworks.

## Examples
See `skills/security-testing/templates/` for example engagements.
```

**Result:** 185 lines → 147 lines (38 lines saved, zero information lost)

---

## Enforcement History

### Why 150 Lines?

**Token efficiency:**
- Agent files are loaded into context for every task
- Smaller agents = less token usage per invocation
- 150 lines ≈ 3000-4000 tokens (acceptable overhead)

**Maintainability:**
- Easier to read and understand
- Faster to locate routing logic
- Less duplication across agents

**Quality:**
- Forces proper separation of concerns
- Prevents agents from becoming "skill files"
- Encourages use of progressive disclosure

### Violation History

**Before enforcement (2025-12-11):**
- Some agents were 200-300 lines
- Contained inlined workflows
- Duplicated content between agents
- Hard to maintain

**After enforcement (2025-12-17):**
- All agents <150 lines
- Workflows extracted to skills/
- Clear references to detailed docs
- Easy to maintain

---

## Template

**Use official template:**
```bash
cp library/templates/AGENT-TEMPLATE.md agents/new-agent.md
```

**Template includes:**
- Proper structure (6 required sections)
- Line count annotations
- Reference patterns
- Example routing logic

---

## Related Documentation

- `docs/agent-routing-architecture.md` - Routing patterns and decision trees
- `docs/hierarchical-context-loading.md` - Progressive disclosure architecture
- `library/templates/AGENT-TEMPLATE.md` - Official agent template
- `library/prompts/format-guardian.md` - Format enforcement reminder

---

**Version:** 1.0
**Last Updated:** 2025-12-17
**Enforcement:** MANDATORY
**Framework:** Intelligence Adjacent (IA) v1.0.0
