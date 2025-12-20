# Technical Documentation Workflow

**Diátaxis Framework implementation for framework documentation**

**Purpose:** Create clear, structured, purpose-driven documentation

---

## Diátaxis Framework (4 Documentation Types)

**Framework:** Divio's Diátaxis (https://diataxis.fr/)

| Intent | Type | User Asks | Characteristics |
|--------|------|-----------|-----------------|
| Learning | **Tutorial** | "How do I learn X?" | Learning-oriented, step-by-step, works when followed |
| Goal | **How-To** | "How do I solve Y?" | Task-oriented, problem-solving, assumes knowledge |
| Understanding | **Explanation** | "Why does Z work this way?" | Understanding-oriented, clarification, big picture |
| Reference | **Reference** | "What are the parameters?" | Information-oriented, descriptions, specifications |

**Key Principle:** Don't mix types. Each document has ONE purpose.

---

## Type 1: Tutorial (Learning-Oriented)

**User Intent:** "I want to LEARN how to do X"

**Characteristics:**
- Completely self-contained (works start-to-finish)
- Step-by-step instructions
- Explains what's happening at each step
- Gets user to success quickly
- Beginner-friendly (assumes minimal knowledge)

**Structure:**
```markdown
# [Action] Tutorial

**What you'll learn:** [Specific outcome]
**Prerequisites:** [Minimal - be specific]
**Time:** [Realistic estimate]

## Before You Begin
[Required setup, installations]

## Step 1: [First Action]
[Explanation of what we're doing]

`[Command or code to run]`

[What you should see]
[Why this matters]

## Step 2: [Next Action]
...

## What You Learned
[Summary of concepts covered]

## Next Steps
→ [How-to guide for advanced usage]
→ [Reference for complete options]
```

**Examples:**
- "Getting Started with Claude Code Tutorial"
- "Setting Up Your First Pentest Engagement"
- "Creating a Security Skill from Scratch"

**Location:** `docs/tutorials/`

---

## Type 2: How-To Guide (Task-Oriented)

**User Intent:** "I need to SOLVE a specific problem"

**Characteristics:**
- Focused on accomplishing specific task
- Assumes user has basic knowledge
- Problem-solving oriented
- Multiple approaches acceptable
- No unnecessary explanation (link to explanations)

**Structure:**
```markdown
# How to [Accomplish Specific Task]

**Goal:** [What you'll accomplish]
**Assumes:** [Prerequisites knowledge/setup]

## Option 1: [Recommended Approach]
[When to use this]

1. [Step]
2. [Step]
3. [Step]

## Option 2: [Alternative Approach]
[When to use this instead]

1. [Step]
2. [Step]

## Troubleshooting
**Problem:** [Common issue]
**Solution:** [How to fix]

## Related
→ [Tutorial] for learning basics
→ [Reference] for all options
→ [Explanation] for why this works
```

**Examples:**
- "How to Add a New Slash Command"
- "How to Integrate an MCP Server"
- "How to Fix Hardcoded Count Violations"

**Location:** `docs/how-to/`

---

## Type 3: Explanation (Understanding-Oriented)

**User Intent:** "I want to UNDERSTAND why this works"

**Characteristics:**
- Clarifies and illuminates
- Provides context and background
- Discusses alternatives and trade-offs
- Big picture view
- No step-by-step instructions (that's tutorials/how-tos)

**Structure:**
```markdown
# Understanding [Concept]

## The Problem
[What problem does this solve?]
[Why do we need this?]

## How It Works
[Conceptual explanation]
[Key principles]

## Design Decisions
**Why [choice A] over [choice B]?**
[Trade-offs considered]
[Rationale]

## Implications
[What this means for users]
[What this means for developers]

## Alternatives Considered
[Other approaches evaluated]
[Why this approach chosen]

## Related Concepts
→ [Tutorial] to try it
→ [How-to] to use it
→ [Reference] for details
```

**Examples:**
- "Understanding Hierarchical Context Loading"
- "Why Agent Format Limits Matter"
- "The Intelligence Adjacent Philosophy"

**Location:** `docs/explanations/`

---

## Type 4: Reference (Information-Oriented)

**User Intent:** "What are the available options/parameters?"

**Characteristics:**
- Dry, factual, precise
- Complete and accurate
- Structured for lookup (not reading)
- No explanations (link to explanations)
- Authoritative

**Structure:**
```markdown
# [Component] Reference

## Overview
[Brief description - 1-2 sentences]

## Parameters

### parameter_name
- **Type:** string | number | boolean
- **Required:** Yes | No
- **Default:** [value]
- **Description:** [What it does]
- **Example:** `parameter_name: "value"`

## Methods

### methodName()
**Signature:** `methodName(param1: string, param2?: number): ReturnType`

**Parameters:**
- `param1` (string, required) - [Description]
- `param2` (number, optional) - [Description]

**Returns:** [Return value description]

**Example:**
`[Code example]`

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option1 | string | "default" | [Description] |
| option2 | boolean | false | [Description] |

## See Also
→ [Tutorial] to learn basics
→ [How-to] for common tasks
→ [Explanation] to understand design
```

**Examples:**
- "Slash Commands Reference"
- "Skill YAML Frontmatter Reference"
- "Agent Invocation API Reference"

**Location:** `docs/reference/`

---

## Writing Process

### 1. Identify Documentation Type

**Ask:** What is the user's PRIMARY intent?
- Learn? → Tutorial
- Solve? → How-To
- Understand? → Explanation
- Lookup? → Reference

**If mixed intent:** Create multiple documents, link between them

### 2. Follow Template

**Use strict template for chosen type:**
- Tutorial: Step-by-step with explanations
- How-To: Goal-focused with options
- Explanation: Conceptual with rationale
- Reference: Structured specifications

### 3. Validation Checklist

**Before publishing:**
- [ ] Single type only (not mixed)
- [ ] Appropriate tone for type
- [ ] Complete for its purpose
- [ ] Links to related docs
- [ ] Code examples work
- [ ] Accurate information

### 4. Cross-Linking

**Every document should link to:**
- Tutorial (learn it)
- How-To (use it)
- Explanation (understand it)
- Reference (look it up)

**Example:**
```markdown
## See Also
→ [Tutorial: Getting Started](#) - Learn the basics
→ [How-To: Common Tasks](#) - Solve specific problems
→ [Explanation: Why This Design](#) - Understand the rationale
→ [Reference: Complete API](#) - All parameters and options
```

---

## Common Mistakes

### ❌ Mixing Types

**Bad:** Tutorial that includes reference details
**Good:** Tutorial focused on learning, links to reference

### ❌ Wrong Tone

**Bad:** Reference with conversational explanations
**Good:** Reference with dry, factual descriptions (link to explanation)

### ❌ Incomplete Purpose

**Bad:** How-to that stops at "now you understand the concept"
**Good:** How-to that completes the actual task

### ❌ No Cross-Links

**Bad:** Standalone document with no navigation
**Good:** Document linked to related type-specific docs

---

## Quality Standards

**Tutorial Standards:**
- Must work when followed exactly
- Complete from start to finish
- Beginner can succeed

**How-To Standards:**
- Accomplishes stated goal
- Multiple viable options shown
- Troubleshooting included

**Explanation Standards:**
- Clarifies concepts thoroughly
- Provides context and rationale
- Big picture view maintained

**Reference Standards:**
- 100% accurate and complete
- Structured for quick lookup
- No opinions or explanations

---

## File Organization

```
docs/
├── tutorials/
│   ├── getting-started.md
│   ├── first-skill.md
│   └── first-agent.md
├── how-to/
│   ├── add-command.md
│   ├── integrate-mcp.md
│   └── fix-violations.md
├── explanations/
│   ├── hierarchical-loading.md
│   ├── agent-format.md
│   └── ia-philosophy.md
└── reference/
    ├── commands-reference.md
    ├── skill-yaml.md
    └── agent-api.md
```

---

## Special Case: README Files

**README.md serves as navigation hub** - Can mix types but MUST:
- Clearly label each section
- Keep each section focused
- Link to dedicated docs for detail

**Example README structure:**
```markdown
# Component Name

[Brief explanation]

## Quick Start (Tutorial-style)
[Minimal steps to get working]
→ See full tutorial: [Link]

## Common Tasks (How-To style)
- [Task 1] - [Link to how-to]
- [Task 2] - [Link to how-to]

## Understanding [Concept] (Explanation-style link)
→ See explanation: [Link]

## Reference
→ Complete reference: [Link]
```

---

**See Also:**
- [Diátaxis Framework](https://diataxis.fr/) - Official documentation
- `reference/writing-standards.md` - Style guide
- `library/prompts/content-guardian.md` - Validation rules
