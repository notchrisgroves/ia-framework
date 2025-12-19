---
type: documentation
title: Agent Routing Architecture
classification: public
version: 2.0
last_updated: 2025-12-11
---

# Agent Routing Architecture

**Version:** 2.0
**Updated:** 2025-12-11
**Purpose:** Documentation for 4-agent routing architecture

---

## Overview

The Intelligence Adjacent framework uses a **simplified 4-agent architecture** where base Claude Code handles simple operations and specialized agents handle domain-specific work.

---

## Current Architecture

```
User Request
     ↓
[Base Claude] ← Handles simple operations (file ops, git, navigation)
     ↓
[Domain Analysis] ← Matches request to specialized domain
     ↓
[Specialized Agent] ← security | writer | advisor | legal
     ↓
[Expert Execution] ← Agent loads skills and executes workflow
```

### 4 Specialized Agents

1. **security** - All security operations (pentesting, code review, architecture, compliance)
2. **writer** - Content creation (blog posts, technical docs, security reports)
3. **advisor** - Personal development, OSINT research, QA review
4. **legal** - Legal compliance with mandatory citation verification

**Invocation:** `Task(subagent_type="agent-name", prompt="...")`

---

## Routing Logic

### When Base Claude Handles Directly

**Simple Operations:**
- File reads: "read CLAUDE.md"
- Git status: "git status"
- Directory listings: "ls skills/"
- Simple searches: "find files with TODO"
- Documentation: "update README.md"

### When Base Claude Delegates to Agents

**Security Work → security agent:**
- Penetration testing
- Code review for vulnerabilities
- Architecture security assessment
- Compliance validation (CIS, STIG, OWASP)
- Threat intelligence gathering

**Content Creation → writer agent:**
- Blog posts
- Technical documentation
- Security reports
- Newsletter generation

**Advisory/Research → advisor agent:**
- Career development (job applications, resume review, interview prep)
- OSINT research
- QA review (blog posts, documentation, code)
- Personal coaching (CliftonStrengths-based)

**Legal Compliance → legal agent:**
- GDPR, CCPA, privacy compliance
- Risk assessments
- Jurisdictional research
- Policy review
- **Always with mandatory citation verification**

---

## Enforcement Mechanisms

### 1. Agent Prompts (Primary Enforcement)

**Location:** `agents/*.md` files

**Method:** Each agent has MANDATORY sections defining:
- QA review requirements (writer: rating ≥4 before publishing)
- File organization rules (FILE-LOCATION-STANDARDS.md)
- Session state protocols
- Workflow phase requirements

**Advantage:** Self-enforcing through agent identity and memory

### 2. Pre-Commit Hooks (Git-Level Enforcement)

**Location:** `.git/hooks/pre-commit`

**Enforces:**
- Agent format validation (150-line limit)
- Credential scanning (blocks hardcoded API keys)

**Status:** ✅ Active and working (when migrated)

### 3. Documentation Standards

**Location:** `docs/*.md` files

**Standards:**
- FILE-LOCATION-STANDARDS.md (where files belong)
- session-checkpoint-enforcement.md (multi-session protocol)
- CREDENTIAL-HANDLING-ENFORCEMENT.md (credential management)

**Advantage:** Clear reference documentation, agent memory enforces compliance

---

## Quality Maintenance

**Quality maintained through:**
- Clear agent instructions (MANDATORY sections in agent.md files)
- Skill workflow definitions (sequential phases defined in SKILL.md)
- Documentation standards (FILE-LOCATION-STANDARDS, session protocol)
- Agent invocation rules (proper delegation to specialized agents)
- Pre-commit validation (format checks, credential scanning)

**See:** `docs/session-checkpoint-enforcement.md` for session protocol

---

## Historical Note

**Previous Architecture (v1.0 - Nov 2025):**
- Included director agent as mandatory routing layer
- mandatory-director-router.ts hook enforced director usage
- Layer 0 enforcement with keyword patterns
- All complex requests forced through director first

**Rationale for Change:**
- Director agent was redundant orchestration layer
- Base Claude can analyze domains and route directly
- Simplified architecture is more maintainable
- Reduced cognitive overhead for users
- Same quality enforcement through agent prompts and documentation

---

## Related Documentation

- **Agent Files:** `agents/security.md`, `agents/writer.md`, `agents/advisor.md`, `agents/legal.md`
- **Skill Registry:** `skills/*/SKILL.md` files
- **Tool Catalog:** `library/catalogs/TOOL-CATALOG.md`
- **CLAUDE.md:** Section "Agent Invocation Rules"

---

**Version:** 2.0 (Simplified to 4-agent architecture)
**Last Updated:** 2025-12-11
**Framework:** Intelligence Adjacent (IA)
