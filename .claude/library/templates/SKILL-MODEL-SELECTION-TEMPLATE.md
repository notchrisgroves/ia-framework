# Model Selection Template for Skills

**Purpose:** Standard section to add to all SKILL.md files for consistent model selection guidance

**Location in SKILL.md:** After "Critical Rules" section, before "Decision Tree"

---

## Template

```markdown
---

## Model Selection

**Reference:** See `library/model-selection-matrix.md` for complete task-to-model mapping

**Skill-Specific Guidance:**

### Default Model
**Latest Sonnet** - Balanced performance for most {skill-name} tasks

### Upgrade to Opus When:
- [Specific scenario requiring frontier reasoning]
- [Novel problem type]
- [Complex decision requiring deep analysis]

### Downgrade to Haiku When:
- [Simple/template operations]
- [Checklist execution]
- [Format validation]

### Specialized Models:
- **Latest Grok Code** - [When reasoning traces needed, e.g., vulnerability analysis]
- **Latest Grok 4.1** - [When deep research/large context needed]
- **Latest Grok 3** - [When adversarial review needed]
- **Perplexity Sonar-Pro** - [When OSINT/real-time research needed]

**Dynamic Selection:** All models use `tools/research/openrouter/fetch_models.py` for latest versions

---
```

---

## Examples by Skill Type

### Security Skills (security-testing, code-review, architecture-review)

```markdown
## Model Selection

**Reference:** See `library/model-selection-matrix.md` for complete task-to-model mapping

**Skill-Specific Guidance:**

### Default Model
**Latest Sonnet** - Handles most security testing and analysis

### Upgrade to Opus When:
- Novel attack vectors or zero-day research
- Complex threat modeling requiring strategic analysis
- Multi-stage attack chain planning
- Architecture security design decisions

### Downgrade to Haiku When:
- Standards compliance checks (CIS, STIG)
- Format validation of security reports
- Checklist-based audits
- Simple reconnaissance tasks

### Specialized Models:
- **Latest Grok Code** - Security code review (reasoning traces explain WHY vulnerable)
- **Latest Grok 4.1** - Deep threat intelligence research (2M context)
- **Perplexity Sonar-Pro** - OSINT reconnaissance, CVE research

**Dynamic Selection:** All models use `tools/research/openrouter/fetch_models.py` for latest versions

---
```

### Content Skills (writer, technical-writing, report-generation)

```markdown
## Model Selection

**Reference:** See `library/model-selection-matrix.md` for complete task-to-model mapping

**Skill-Specific Guidance:**

### Default Model
**Latest Sonnet** - Quality writing and documentation

### Upgrade to Opus When:
- Novel content requiring strategic thinking
- Complex technical explanations
- Architecture documentation
- Long-form investigative pieces

### Downgrade to Haiku When:
- Template application
- Format validation
- Checklist-based QA
- Simple edits and corrections

### Specialized Models:
- **Perplexity Sonar-Pro** - Research phase (citations, current events)
- **Latest Grok 3** - Adversarial review (challenge assumptions)

**Workflow Pattern:** Perplexity (research) → Sonnet (write) → Haiku (QA) + Grok 3 (adversarial QA)

**Dynamic Selection:** All models use `tools/research/openrouter/fetch_models.py` for latest versions

---
```

### Research Skills (osint-research, threat-intel)

```markdown
## Model Selection

**Reference:** See `library/model-selection-matrix.md` for complete task-to-model mapping

**Skill-Specific Guidance:**

### Default Model
**Perplexity Sonar-Pro** - Primary OSINT research with citations

### Secondary Model
**Latest Grok 4.1 Fast** - Deep analysis and cross-validation (2M context)

### Upgrade to Opus When:
- Strategic intelligence synthesis
- Complex geopolitical analysis
- Novel threat pattern identification

### Research Pattern:
- **Fast Mode:** Perplexity only (5-10 min)
- **Deep Mode:** Perplexity + Grok 4.1 (dual-source cross-validation)

**Dynamic Selection:** All models use `tools/research/openrouter/fetch_models.py` for latest versions

---
```

### Advisory Skills (qa-review, career, legal)

```markdown
## Model Selection

**Reference:** See `library/model-selection-matrix.md` for complete task-to-model mapping

**Skill-Specific Guidance:**

### Dual-Model Pattern
- **Latest Haiku** - Structured review (checklists, standards)
- **Latest Grok 3** - Adversarial review (challenge assumptions)

### Default Model
**Latest Sonnet** - General advisory work

### Upgrade to Opus When:
- Complex career strategy decisions
- Novel legal compliance scenarios
- Strategic risk assessments

### Downgrade to Haiku When:
- Format checks
- Completeness validation
- Checklist execution

**Dynamic Selection:** All models use `tools/research/openrouter/fetch_models.py` for latest versions

---
```

### Meta Skills (create-skill, gitingest-repo)

```markdown
## Model Selection

**Reference:** See `library/model-selection-matrix.md` for complete task-to-model mapping

**Skill-Specific Guidance:**

### Default Model
**Latest Haiku** - Template application and file organization

### Upgrade to Sonnet When:
- Custom workflow design
- Complex skill architecture
- Integration planning

### Upgrade to Opus When:
- Novel framework patterns
- Strategic architecture decisions

**Dynamic Selection:** All models use `tools/research/openrouter/fetch_models.py` for latest versions

---
```

---

## Implementation Checklist

When adding model selection to a skill:

- [ ] Add section after "Critical Rules", before "Decision Tree"
- [ ] Choose appropriate template based on skill type
- [ ] Customize scenarios to match skill's specific tasks
- [ ] Ensure "Dynamic Selection" reference included
- [ ] Keep total SKILL.md under 500 lines
- [ ] Reference matrix for detailed guidance
- [ ] Test model selection makes sense for skill workflows

---

**Version:** 1.0
**Created:** 2025-12-16
**Authority:** `library/model-selection-matrix.md`
