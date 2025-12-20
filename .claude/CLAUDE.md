# Intelligence Adjacent (IA) Framework

**Building systems that augment human intelligence, not replace it.**

---

## System Configuration

**Environment:** Claude Code | **Root:** Current working directory | **Platform:** Cross-platform

**Installation:** See `README.md` | **Health Check:** `python tools/validation/framework-health-check.py`

---

## System Philosophy

**Intelligence Adjacent (IA)** - Systems that work alongside human intelligence, not replace it.

**Core Principles:** Solve once/reuse forever, file-based context, skills-based architecture, human augmentation

**Hierarchical Context Loading:**
```
Level 1: CLAUDE.md (<150 lines, navigation) ← YOU ARE HERE
Level 2: skills/*/SKILL.md (<500 lines, complete skill)
Level 3: agents/*.md (<150 lines, identity + routing)
```

See `docs/hierarchical-context-loading.md`

---

## Agent Routing

**Base Claude handles basic operations** - Specialized work routes to agents

**Routing Rules:**
- Security (pentesting, code review, architecture) → security agent
- Content (blog, docs, reports) → writer agent
- Advisory/Research (OSINT, career, QA) → advisor agent
- Legal (GDPR, privacy, risk) → legal agent
- Basic file ops, git, navigation → Base Claude (no delegation)

**Invocation:** `Task(subagent_type="agent-name")`

---

## Critical Requirements

### Tool Discovery

**BEFORE delegating or creating tools:** Read `library/catalogs/TOOL-CATALOG.md`, search `skills/*/scripts/**`, verify availability

**Tool Organization:** `tools/` (framework-core) | `skills/{skill}/scripts/` (skill-specific) | `servers/` (VPS wrappers)

### Agent Format

**Agents MUST be <150 lines** (pre-commit hook enforced). Follow `library/templates/AGENT-TEMPLATE.md`

**Before editing:** Read `library/prompts/content-guardian.md`, check line count, validate with `python tools/validation/lint-agents.py`

See `docs/AGENT-FORMAT-STANDARDS.md`

### Session Checkpoints

**Multi-session projects MUST maintain SESSION-STATE.md** at `sessions/YYYY-MM-DD-project-name.md`

Template: `library/templates/SESSION-STATE-TEMPLATE.md`

See `docs/session-checkpoint-enforcement.md`

### Credential Security

**ALL scripts load credentials from `.env` ONLY** - No hardcoded keys, no fallbacks, pre-commit hook blocks violations

Templates: `tools/_*-CREDENTIAL-TEMPLATE.*`

See `docs/CREDENTIAL-HANDLING-ENFORCEMENT.md`

---

## Directory Structure

```
ia-framework/
├── CLAUDE.md                     (This file - navigation)
├── BACKLOG.md                    (Task tracking - check before starting work)
├── .env                          (API keys - gitignored)
├── settings.json                 (Framework config)
├── agents/                       (Specialized agents)
├── skills/                       (Modular capabilities)
├── commands/                     (Slash commands)
├── plans/                        (Design documents - gitignored)
├── sessions/                     (Session tracking - gitignored)
├── output/                       (Engagement deliverables - gitignored)
│   ├── engagements/[type]/[id]/  (Client work outputs)
│   └── blog/[category]/          (Blog content)
├── tools/                        (Framework utilities)
├── library/                      (Shared resources)
├── hooks/                        (Pre-commit validation)
└── docs/                         (Architecture docs)
```

**Output Directory:** All engagement deliverables and blog content go in `output/` (see `docs/FILE-LOCATION-STANDARDS.md`)

**Task Tracking:** Check `BACKLOG.md` for ongoing work before starting new tasks

---

## Agents

**Specialized agents with skill-based context loading:**

- **security** - Security operations (testing, advisory, engineering)
- **writer** - Content creation (blog, docs, reports)
- **advisor** - Personal development + research + QA
- **legal** - Legal compliance with citation verification

See `agents/*.md` and `skills/*/SKILL.md`

---

## Documentation Standards

**NEVER hardcode counts** (e.g., "18 skills") - Creates maintenance debt

**Use:** Qualifiers ("Multiple skills"), descriptive ("Specialized agents"), categories only

**Enforcement:** `python tools/validation/validate-readme.py`, `library/prompts/content-guardian.md`, pre-commit hook

See `docs/README-MAINTENANCE-DESIGN.md`

---

## Security Requirements

**Repository Safety:**
- Run `git remote -v` BEFORE every commit (verify correct repo)
- Review changes before committing to public repos
- CHECK THREE TIMES before git add/commit

**Infrastructure:** EXTREMELY CAUTIOUS with cloud, DNS, production services

**Working Style:** Be concise and direct, focus on practical implementation, build modular solutions, security-first mindset, professional-grade outputs

---

## Reference Documentation

**Architecture:**
- `hierarchical-context-loading.md` - Progressive disclosure
- `agent-routing-architecture.md` - When to invoke which agent
- `FILE-LOCATION-STANDARDS.md` - Where files belong
- `session-checkpoint-enforcement.md` - Multi-session protocol
- `AGENT-FORMAT-STANDARDS.md` - Agent structure requirements
- `CREDENTIAL-HANDLING-ENFORCEMENT.md` - Security standards

**Model Selection:**
- `library/model-selection-matrix.md` - Task-to-model mapping and cost optimization

---

**Version:** 1.0.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
