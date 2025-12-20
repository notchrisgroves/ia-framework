# Skills - Specialized Domain Knowledge

> **Note:** This is a manual reference file for the skills/ subsystem. It is NOT auto-loaded by hooks. Only root CLAUDE.md is auto-loaded on session start.

**Purpose:** Skill files containing decision trees, workflows, and domain-specific expertise

---

## Skill Architecture

**Skills contain:**
- SKILL.md - Main decision tree and routing logic (<500 lines)
- reference/ - Loaded on-demand (frameworks, methodologies, standards)
- scripts/ - Executed tools (not loaded as context)
- workflows/ - Step-by-step processes for specific tasks

**All skills follow official Claude Skills structure**

---

## How Skills Work

**1. Agent routes to skill:**
```python
# In security.md agent
"If task involves pentesting → Load skills/security-testing/SKILL.md"
```

**2. PreToolUse hook loads skill:**
```bash
# hooks/load-agent-skill-context.py fires
# Loads: agents/security.md + skills/security-testing/SKILL.md
# Injects as <system-reminder>
```

**3. Skill decision tree executes:**
```markdown
# In SKILL.md
Mode Detection → Load appropriate workflow → Execute steps → Return results
```

**4. Progressive disclosure:**
- SKILL.md loaded first (routing logic)
- Reference files loaded only if needed (methodologies, frameworks)
- Scripts executed when tools required

---

## Skill Structure (Official Pattern)

```
skills/{name}/
├── SKILL.md              # Decision tree, routing logic (<500 lines)
├── reference/            # On-demand context (frameworks, methodologies)
│   ├── standards.md
│   ├── frameworks.md
│   └── methodologies/
├── scripts/              # Executable tools (not loaded as context)
│   └── tool-name.py
└── workflows/            # Step-by-step processes
    └── workflow-name.md
```

**Key principle:** SKILL.md routes, reference/ provides detail, scripts/ execute actions

---

## Available Skills

**Categories:** Security, Content, Research, Advisory, Infrastructure, Meta

**See:** `ls skills/` for complete list with SKILL.md descriptions

---

## Skill Format Standards

**SKILL.md requirements:**
- YAML frontmatter: name, description only
- Max 500 lines (recommended <400)
- Decision tree routing logic
- Reference external files (don't inline)
- Progressive disclosure pattern

**Example frontmatter:**
```yaml
---
name: security-testing
description: Penetration testing, vulnerability scanning, and network segmentation validation with PTES/OWASP methodologies
---
```

---

## Decision Tree Pattern

**Every SKILL.md should:**

1. **Detect mode/task type:**
```markdown
## Mode Detection
- Pentest keywords → pentest-init workflow
- Vuln scan keywords → vuln-scan workflow
- Segmentation → segmentation-test workflow
```

2. **Load appropriate workflow:**
```markdown
## Workflow Loading
Reference: workflows/pentest-init.md
(Don't inline the full workflow in SKILL.md)
```

3. **Execute and return:**
```markdown
Follow workflow steps → Create deliverables → Update session state
```

---

## When to Create New Skills

**Create new skill when:**
- Domain expertise requires >300 lines of context
- Multiple related workflows share common patterns
- Reusable across different projects
- Has specialized tools/scripts

**DON'T create new skill for:**
- One-off tasks (use existing skill)
- Simple commands (create slash command instead)
- Variations of existing skills (extend existing skill)

---

## Progressive Disclosure

**Load only what's needed:**

**Level 1:** SKILL.md (always loaded)
- Decision tree routing
- Mode detection
- Workflow references

**Level 2:** Workflows (loaded when needed)
- Specific task steps
- Execution sequence
- Deliverable templates

**Level 3:** Reference materials (loaded on-demand)
- Frameworks (PTES, OWASP)
- Methodologies (domain-specific)
- Standards (CIS, NIST)

**Token savings:** 60-80% vs loading everything upfront

---

## Testing Skills

**Manual test:**
```bash
# Invoke via agent
Task(subagent_type="security", prompt="Pentest acme.com")

# Verify:
# - SKILL.md loaded
# - Correct workflow selected
# - Deliverables created in right location
```

**Evaluation suite (future):**
```bash
# Test decision tree routing
python tools/evals/test-skill-routing.py security-testing

# Test workflow execution
python tools/evals/test-workflow.py security-testing/pentest-init
```

---

## Common Issues

**SKILL.md >500 lines:**
- Solution: Extract workflows to workflows/, reference them
- Move detailed methodologies to reference/
- Use progressive disclosure

**Wrong workflow loaded:**
- Check mode detection keywords in SKILL.md
- Update decision tree routing logic

**Duplicate content across skills:**
- Extract shared content to library/
- Reference common frameworks/methodologies
- Don't duplicate, reference

---

## Resources Location

**Shared resources:** `resources/library/` - Discover dynamically with Glob
- Benchmarks: `resources/library/benchmarks/` (CIS controls, hardening)
- Frameworks: `resources/library/frameworks/` (NIST, OWASP, PCI-DSS, HIPAA, GDPR, MITRE)
- Repositories: `resources/library/repositories/` (OWASP cheatsheets, ASVS, WSTG)
- Books: `resources/library/books/` (security methodology references)
- Threat Intel: `resources/library/threat-intelligence/`

**Skill-specific methodologies:** `skills/*/methodologies/` (NOT in resources/library)

**Dynamic discovery:** Use `Glob: resources/library/**/*{keyword}*` - never hardcode paths

---

## References

**Templates:**
- `library/templates/SKILL-TEMPLATE.md` - Skill structure
- `create-skill` skill - Skill creation workflows

**Documentation:**
- `docs/hierarchical-context-loading.md` - Progressive disclosure
- `docs/AGENT-FORMAT-STANDARDS.md` - Related agent standards

**Official:**
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

---

**Skills:** See `ls skills/` for complete list
**Max SKILL.md Lines:** 500 (recommended <400)
**Framework:** Intelligence Adjacent (IA) v1.0.0
