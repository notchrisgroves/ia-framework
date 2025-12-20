# Agents - Specialized Context Routers

> **Note:** This is a manual reference file for the agents/ subsystem. It is NOT auto-loaded by hooks. Only root CLAUDE.md is auto-loaded on session start.

**Purpose:** Agent prompts that route work to appropriate skills based on task type

---

## Agent Architecture

**Available agents:**

| Agent | Domain | Status | Skills Routed |
|-------|--------|--------|---------------|
| security.md | Security operations | ✅ Public | security-testing, code-review, architecture-review, threat-intel, dependency-audit, secure-config, benchmark-generation |
| advisor.md | Personal development + research | ✅ Public | career, osint-research, qa-review |
| writer.md | Content creation | 🧪 Testing | writer, diagram-generation |
| legal.md | Legal compliance | 🧪 Testing | legal |

**Status Legend:** ✅ Public (in public repo) | 🧪 Testing (internal only)

**Core principles:**
- <150 lines per agent (enforced by pre-commit hook)
- Routes to skills based on task keywords/context
- Loads skill context via PreToolUse hook
- References SKILL.md files (no inline workflows)

---

## How Agents Work

1. **User invokes:** `Task(subagent_type="security")` from base Claude
2. **Hook loads:** `agents/security.md` + appropriate `skills/*/SKILL.md`
3. **Agent routes:** Reads task, selects correct skill workflow
4. **Returns:** Results to base Claude

See `docs/agent-routing-architecture.md` for complete routing logic.

---

## Format & Editing

**Format Standards:** See `docs/AGENT-FORMAT-STANDARDS.md` for:
- Structure requirements and line limits
- Required sections (Quick Start, Core Identity, Startup Sequence, etc.)
- Validation commands and enforcement

**Routing Rules:** See `docs/agent-routing-architecture.md` for:
- Complete routing patterns per agent
- Skill mapping and decision trees
- Keyword detection and task routing

**Editing Guidelines:** See `docs/AGENT-FORMAT-STANDARDS.md` for:
- When to edit agents (routing changes, identity updates)
- Pre-edit checklist (line count, format guardian)
- What NOT to edit (workflows, examples, reference materials)

---

## Testing

**Manual test:**
```bash
Task(subagent_type="security", prompt="Test pentest routing")
```

Verify: Agent loaded → Skill context loaded → Correct routing → Results returned

**Validation:** `python tools/validation/lint-agents.py`

---

## Common Issues

**Agent >150 lines:**
- Extract content to SKILL.md and reference it
- Use `python tools/validation/lint-agents.py`

**Wrong skill loaded:**
- Check routing keywords in agent file
- Update decision logic if needed

**Duplicate content:**
- Reference instead of inlining: "See skills/security-testing/SKILL.md"

---

## Files in This Directory

```
agents/
├── CLAUDE.md           (This file - agent system overview)
├── security.md         (Security operations router)
├── writer.md           (Content creation router)
├── advisor.md          (Advisory/research router)
└── legal.md            (Legal compliance router)
```

---

## References

**Templates:**
- `library/templates/AGENT-TEMPLATE.md` - Agent structure template
- `library/prompts/format-guardian.md` - Enforcement reminder

**Documentation:**
- `docs/agent-routing-architecture.md` - Complete routing logic
- `docs/AGENT-FORMAT-STANDARDS.md` - Format requirements
- `docs/hierarchical-context-loading.md` - Context loading system

**Validation:**
- `tools/validation/lint-agents.py` - Agent format validator
- `hooks/pre-commit/` - Pre-commit validation

---

**Agents:** security, writer, advisor, legal
**Max Line Count:** <150 lines (enforced)
**Framework:** Intelligence Adjacent (IA) v1.0.0
