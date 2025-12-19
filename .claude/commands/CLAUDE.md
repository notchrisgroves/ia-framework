# Commands - Slash Command Workflows

> **Note:** This is a manual reference file for the commands/ subsystem. It is NOT auto-loaded by hooks. Only root CLAUDE.md is auto-loaded on session start.

**Purpose:** Guided workflows triggered by `/command-name` syntax

---

## Command Architecture

**Slash commands provide:**
- Guided workflows with step-by-step prompts
- Consistent user experience across tasks
- Self-documenting usage instructions
- Integration with agent/skill system

**Command files:**
- Markdown format with YAML frontmatter
- Usage examples and expected outputs
- Agent routing information
- Input/output specifications

---

## How Commands Work

**1. User types command:**
```bash
/pentest
```

**2. UserPromptSubmit hook detects:**
```python
# hooks/detect-commands.py fires
# Loads commands/pentest.md
# Injects as <system-reminder>
```

**3. Command executes:**
```markdown
# Command file loaded
Agent: security
Skill: security-testing
Workflow: pentest-init

# User prompted for inputs
# Agent invoked with context
# Deliverables created
```

---

## Command Format

**Frontmatter (official fields only):**
```yaml
---
name: command-name
description: Brief description of what command does
---
```

**Removed fields (not in official spec):**
- ❌ agent (use body instead)
- ❌ skill (use body instead)
- ❌ complexity (not needed)
- ❌ version (use git history)

**Body sections:**
1. Quick Start - Basic usage example
2. When to Use - Use cases and anti-patterns
3. Workflow - Step-by-step process
4. Examples - Real usage scenarios
5. References - Related commands/docs

---

## Available Commands

**Security Testing (6):**
- `/pentest` - Penetration testing with Director/Mentor/Demo modes
- `/vuln-scan` - Automated vulnerability scanning
- `/segmentation-test` - Network segmentation validation
- `/code-review` - Security-focused code review
- `/arch-review` - Architecture security with threat modeling
- `/risk-assessment` - Formal cybersecurity risk assessment

**Security Engineering (4):**
- `/secure-config` - Infrastructure hardening validation (CIS/STIG)
- `/dependency-audit` - Supply chain security analysis
- `/benchmark-gen` - Generate CIS/STIG compliance scripts
- `/threat-intel` - Threat intelligence with CVE research

**Career (1):**
- `/job-analysis` - Job posting analysis, resume optimization, interview prep

**Content (2):**
- `/blog-post` - Blog content creation for Intelligence Adjacent
- `/newsletter` - Weekly newsletter digest generation

**Git/Sync (2):**
- `/git-sync` - Git workflow automation (stage, commit, push)
- `/public-sync` - Publish framework to public GitHub

---

## Command Routing

**Each command specifies:**

**Agent:** Which agent handles execution
```markdown
**Agent:** security
```

**Skill:** Which skill provides domain expertise
```markdown
**Skill:** security-testing
```

**Output:** Where results are saved
```markdown
**Output:** output/engagements/pentests/{target}-{YYYY-MM}/
```

---

## Creating New Commands

**Use template:**
```bash
# Copy template
cp library/templates/COMMAND-TEMPLATE.md commands/new-command.md

# Edit frontmatter
# Write workflow steps
# Add examples
# Test execution
```

**Requirements:**
- YAML frontmatter with name + description
- Clear "When to Use" section
- Step-by-step workflow
- Real examples
- Reference to agent/skill

**Validation:**
```bash
# Ensure frontmatter valid
python tools/validation/validate-commands.py
```

---

## Command Best Practices

**DO:**
- ✅ Provide clear Quick Start example
- ✅ Show expected outputs
- ✅ Link to related commands
- ✅ Include time estimates
- ✅ Show Agent and Skill routing

**DON'T:**
- ❌ Inline entire workflows (reference skill files)
- ❌ Duplicate content between commands
- ❌ Use custom frontmatter fields
- ❌ Make commands too complex (split if >200 lines)

---

## Command Detection

**Keyword-based suggestions:**

Hook: `hooks/detect-commands.py`

**Example keywords:**
- "job posting" → Suggests `/job-analysis`
- "pentest" → Suggests `/pentest`
- "blog post" → Suggests `/blog-post`
- "resume" → Suggests `/job-analysis`

**Add new mappings in:**
`hooks/detect-commands.py` KEYWORD_MAP

---

## Testing Commands

**Manual test:**
```bash
# Type command in Claude Code
/pentest

# Verify:
# - Command file loaded
# - Prompts displayed
# - Agent invoked correctly
# - Outputs created in right location
```

**Evaluation test (future):**
```bash
# Test command with various inputs
python tools/evals/test-command.py pentest
```

---

## Output Locations

**Commands use workspace-relative paths:**
- Blog content: `output/blog/`
- Career materials: `output/career/`
- Security engagements: `output/engagements/`
- Research: `output/research/`
- Documentation: `output/documentation/`

**NOT:**
- ❌ `personal/` (doesn't exist in universal framework)
- ❌ `professional/` (doesn't exist in universal framework)
- ❌ Skill-internal paths like `skills/*/output/`

---

## Files in This Directory

```
commands/
├── CLAUDE.md           (This file - command system overview)
├── pentest.md          (Penetration testing)
├── blog-post.md        (Blog content creation)
├── job-analysis.md     (Job application analysis)
├── ... (15 total commands)
```

---

## References

**Templates:**
- `library/templates/COMMAND-TEMPLATE.md` - Command structure

**Documentation:**
- `docs/slash-command-architecture.md` - 5-tier architecture
- `README.md` - Complete command listing

**Tools:**
- `hooks/detect-commands.py` - Keyword detection
- `tools/validation/validate-commands.py` - Format validation

---

**Command Count:** Multiple specialized commands (see list above)
**Format:** Markdown with YAML frontmatter
**Framework:** Intelligence Adjacent (IA) v4.0
