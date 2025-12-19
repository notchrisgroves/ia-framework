---
name: create-skill
description: Meta-skill providing templates and patterns for creating new skills, agents, server tools, commands, hooks, and workflows. Contains component templates, structure standards, and framework discovery system patterns. Use when building new framework components.
---

# Create-Skill Meta-Skill

**Meta-skill for creating new framework components**

Provides templates and patterns for creating new skills, agents, server tools, commands, hooks, and other framework components.

**Core Philosophy:** Template-driven development. Follow pattern → Copy template → Fill in → Drop in location → Auto-discovered. No hardcoded registries.

---

## When to Use This Meta-Skill

**Use create-skill when:**
- Creating a new skill for specialized capability
- Building a new agent with unified workflows
- Adding a VPS tool wrapper (Code API pattern)
- Creating new slash commands or hooks
- Documenting a new workflow pattern
- Extending the framework with new component types

**This is NOT a skill loaded by agents** - It's a meta-skill containing templates for building NEW skills.

---

## Framework Discovery System

**7 Discoverable Component Types:**

1. **Skills** - Specialized capabilities loaded by agents (SKILL.md + manifest.yaml)
2. **Agents** - Autonomous workers with specific domains (agent.md with frontmatter)
3. **Server Tools** - VPS tool wrappers (manifest.yaml in servers/)
4. **Commands** - Slash commands for quick actions (.md files in commands/)
5. **Hooks** - Event-triggered automation (.md files in hooks/)
6. **Tools** - Executable utilities (scripts in tools/)
7. **Workflows** - Multi-step processes (workflow.md in skill workflows/)

**Discovery Pattern:**
```
Component Template → Fill in → Drop in location → Auto-discovered
```

**No hardcoded registries. Zero-maintenance scaling.**

**See:** `~/ia-framework/README.md` for complete framework documentation

---

## Template Directory Structure

```
skills/create-skill/templates/
├── SKILL-TEMPLATE.md              (Skill structure)
├── SKILL-MANIFEST-TEMPLATE.yaml   (Skill manifest)
├── AGENT-TEMPLATE.md              (Agent prompt structure)
├── SERVER-TOOL-TEMPLATE/          (VPS Code API wrapper)
├── COMMAND-TEMPLATE.md            (Slash command)
├── HOOK-TEMPLATE.md               (Event automation)
├── WORKFLOW-TEMPLATE.md           (Multi-step process)
├── EVALUATION-TEMPLATE.json       (Skill evaluation)
└── SESSION-STATE-TEMPLATE.md      (Multi-session checkpoint)
```

**All templates follow framework standards** - Line limits, progressive disclosure, decision tree routing

---

## Critical Rules for Component Creation

1. **Always Use Templates** - Ensures consistency, includes all required sections
2. **Follow YAML Manifest Structure** - All discoverable components need manifest/frontmatter
3. **Keep SKILL.md Under 500 Lines** - Navigation layer, extract details to separate files
4. **Progressive Disclosure** - Load only what's needed (SKILL.md → workflows → methodologies)
5. **Update Framework Documentation** - When adding new component types, update README.md

---

## Creating a New Skill

**Follow this workflow:**

### Step 1: Copy Template

```bash
cp skills/create-skill/templates/SKILL-TEMPLATE.md skills/[skill-name]/SKILL.md
cp skills/create-skill/templates/SKILL-MANIFEST-TEMPLATE.yaml skills/[skill-name]/manifest.yaml
```

### Step 2: Fill In Metadata

**SKILL.md frontmatter:**
```yaml
---
name: [skill-name]
description: [One-line description]
version: 1.0
modes:
  - [mode-1]
  - [mode-2]
classification: public
last_updated: [YYYY-MM-DD]
---
```

**manifest.yaml:**
```yaml
---
type: skill
name: [skill-name]
version: 1.0
classification: public
last_updated: [YYYY-MM-DD]
description: |
  [Multi-line description]
modes:
  - [mode-1]
  - [mode-2]
---
```

### Step 3: Build Decision Tree

**Add mode detection logic:**
```markdown
## Decision Tree: Mode Selection

**Level 1: What TYPE of [domain] work?**

### Mode 1: [Mode Name]

**Detection Keywords:**
- User: "[keyword1]", "[keyword2]", "[keyword3]"

**Decision Path:** [Mode] → [Sub-routing] → `workflows/[mode].md`
```

### Step 4: Create Supporting Files

**Required directory structure:**
```
skills/[skill-name]/
├── SKILL.md                 (Navigation layer, <500 lines)
├── manifest.yaml            (Discovery metadata)
├── workflows/               (Step-by-step processes)
├── reference/               (Standards, frameworks)
├── methodologies/           (Detailed approaches)
├── templates/               (Document templates)
└── evals/                   (Skill evaluations)
```

### Step 5: Write Evaluations

**Create 2-3 eval files:**
- eval-001-[mode-1].json
- eval-002-[mode-2].json
- eval-003-[integration-test].json

**Use:** `templates/EVALUATION-TEMPLATE.json`

### Step 6: Drop in Location

```bash
# Skill is now auto-discovered by the framework
# No registration needed
```

**See:** `templates/SKILL-TEMPLATE.md` for complete structure

---

## Creating a New Agent

**Follow this workflow:**

### Step 1: Copy Template

```bash
cp skills/create-skill/templates/AGENT-TEMPLATE.md agents/[agent-name].md
```

### Step 2: Fill In Agent Identity

**Agent frontmatter:**
```markdown
---
agent: [agent-name]
version: 1.0
skills:
  - [skill-1]
  - [skill-2]
max_length: 250
last_updated: [YYYY-MM-DD]
---

# [Agent Name] Agent

**Auto-invoked for [domain] work**

[1-2 sentence description]

**Skills Loaded:** [skill-1], [skill-2]

**Core Philosophy:** [1 sentence]
```

### Step 3: Add Critical Rules

**5 non-negotiable rules:**
```markdown
## 🚨 Critical Rules

1. **Rule 1** - [Description]
2. **Rule 2** - [Description]
3. **Rule 3** - [Description]
4. **Rule 4** - [Description]
5. **Rule 5** - [Description]
```

### Step 4: Add Skill Loading Logic

```markdown
## Skill Loading

**Based on task type, load appropriate skill:**

- [Task type 1] → Load `skills/[skill-1]/SKILL.md`
- [Task type 2] → Load `skills/[skill-2]/SKILL.md`
```

### Step 5: Validate Line Count

```bash
wc -l agents/[agent-name].md
# MUST be ≤ 250 lines
```

**See:** `templates/AGENT-TEMPLATE.md` for complete structure

---

## Creating a Server Tool (VPS Code API)

**VPS Code API wrappers for security tools:**

### Step 1: Copy Template

```bash
cp -r skills/create-skill/templates/SERVER-TOOL-TEMPLATE servers/[tool-name]
```

### Step 2: Fill In Manifest

**manifest.yaml:**
```yaml
---
type: server-tool
name: [tool-name]
version: 1.0
deployment: vps
access_method: code-api
description: |
  [Tool description]
wrapper_type: http-api
---
```

### Step 3: Build Code API Wrapper

**Standard pattern:**
```python
# api.py - FastAPI wrapper
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="[Tool] API")

class ScanRequest(BaseModel):
    target: str
    options: dict = {}

@app.post("/scan")
async def scan(request: ScanRequest):
    # Execute tool
    # Parse output
    # Return JSON
    return {"status": "success", "results": []}
```

### Step 4: Add Deployment

**Docker Compose:**
```yaml
version: '3.8'
services:
  [tool-name]:
    build: .
    ports:
      - "8000:8000"
    networks:
      - app-network
```

**See:** `templates/SERVER-TOOL-TEMPLATE/` for complete structure

---

## Creating a Slash Command

### Step 1: Copy Template

```bash
cp skills/create-skill/templates/COMMAND-TEMPLATE.md commands/[command-name].md
```

### Step 2: Fill In Command

```markdown
---
command: /[command-name]
description: [One-line description]
skill: [associated-skill]
agent: [agent-to-invoke]
---

# /[command-name] - [Short Description]

**Purpose:** [What this command does]

**Agent Invoked:** [agent-name]
**Skill Loaded:** [skill-name]

## Workflow

1. Collect context
2. Invoke [agent] with [skill]
3. Execute [workflow]
4. Deliver results

## Example Usage

User: /[command-name] [args]
Agent: [Response]
```

**See:** `templates/COMMAND-TEMPLATE.md` for complete structure

---

## Line Count Limits (MANDATORY)

**Framework standards:**
- CLAUDE.md: ≤ 250 lines (navigation layer)
- SKILL.md: ≤ 500 lines (skill context)
- Agent prompts: ≤ 250 lines (agent identity)
- Workflows: No limit (detailed processes)
- Reference docs: No limit (standards, frameworks)

**Enforcement:**
- Pre-commit hook validates agent line counts (250 max)
- SKILL.md should be under 500 (manually enforced)

---

## Progressive Disclosure Pattern

**Follow v2.0 architecture:**

**Level 1: CLAUDE.md (250 lines)**
- Framework navigation
- Skill discovery
- Agent routing
- Critical rules

**Level 2: SKILL.md (500 lines)**
- Skill purpose
- Decision tree routing
- Mode detection
- Workflow references

**Level 3: Workflows, Methodologies, Reference**
- Detailed processes
- Standards documentation
- Framework mappings
- Templates

**Load only what's needed for current task**

---

## Testing New Components

**Create evaluations:**

1. **Skill Evaluations** - Test mode routing, workflow execution
2. **Agent Evaluations** - Test skill loading, task routing
3. **Integration Tests** - Test inter-skill communication

**Use:** `templates/EVALUATION-TEMPLATE.json`

---

## Common Patterns

**Pattern 1: Decision Tree Routing**
- All skills use decision tree for mode selection
- Keywords trigger routing to appropriate workflow

**Pattern 2: Progressive Disclosure**
- SKILL.md = navigation layer
- Workflows = detailed processes
- Reference = standards and frameworks

**Pattern 3: Workflow Phases**
- All workflows have clear phases (COLLECT → ANALYZE → DELIVER)
- Checkpoints for multi-session work (Deep Mode only)

**Pattern 4: Fast Mode Default**
- 90% of work uses Fast Mode (no checkpoints)
- Deep Mode opt-in for multi-week projects

---

## Framework Standards

**YAML Manifests:**
- All discoverable components need manifest or frontmatter
- Required fields: type, name, version, description

**Line Limits:**
- CLAUDE.md: ≤ 250 lines
- Agent prompts: ≤ 250 lines
- SKILL.md: ≤ 500 lines

**Directory Structure:**
- skills/[skill-name]/SKILL.md (main file)
- skills/[skill-name]/manifest.yaml (discovery metadata)
- skills/[skill-name]/workflows/ (processes)
- skills/[skill-name]/reference/ (standards)

**Naming Conventions:**
- Skills: lowercase-with-dashes
- Agents: lowercase (security, writer, advisor, legal)
- Commands: /lowercase-with-dashes
- Hooks: event-name.md

---

## Templates Reference

| Template | Purpose | Location |
|----------|---------|----------|
| SKILL-TEMPLATE.md | Skill structure | `templates/` |
| SKILL-MANIFEST-TEMPLATE.yaml | Skill manifest | `templates/` |
| AGENT-TEMPLATE.md | Agent prompt | `templates/` |
| SERVER-TOOL-TEMPLATE/ | VPS Code API wrapper | `templates/` |
| COMMAND-TEMPLATE.md | Slash command | `templates/` |
| HOOK-TEMPLATE.md | Event automation | `templates/` |
| WORKFLOW-TEMPLATE.md | Multi-step process | `templates/` |
| EVALUATION-TEMPLATE.json | Skill evaluation | `templates/` |
| SESSION-STATE-TEMPLATE.md | Multi-session checkpoint | `templates/` |

---

## Examples

**See `examples/` directory for:**
- example-skill/ - Complete skill implementation
- example-agent.md - Agent prompt example
- example-command.md - Slash command example

---

## Version History

**v2.0 (2025-12-11)** - Fresh framework rebuild
- Template-driven component creation
- 7 discoverable component types
- Progressive disclosure architecture
- Line limit enforcement

---

**Version:** 2.0
**Last Updated:** 2025-12-11
**Status:** Meta-skill for framework component creation
