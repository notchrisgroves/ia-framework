---
name: security-advice
description: Quick security guidance on specific topics with framework-based best practices
---

# /security-advice - Security Guidance

Quick, framework-based security guidance for specific questions without formal assessment overhead.

**Agent:** security
**Skill:** security-advisory
**Output:** Conversational (no formal deliverables)

---

## Quick Start

```
/security-advice
```

Collects topic context → Explores relevant library resources → Provides framework-based guidance

---

## When to Use

**Use /security-advice when:**
- Quick security best practices questions
- "How do I secure X?" questions
- Framework guidance (NIST, OWASP, CIS)
- Policy or process recommendations
- Compliance clarifications
- Architecture security questions

**Don't use if:**
- Need formal risk assessment with deliverables → use `/risk-assessment`
- Need hands-on penetration testing → use `/pentest`
- Need vulnerability scanning → use `/vuln-scan`
- Need architecture threat modeling → use `/arch-review`

---

## Workflow

1. **Understand** - Clarify question and context
2. **Research** - Explore `resources/library/` for relevant frameworks, methodologies, benchmarks
3. **Guide** - Provide framework-based guidance with citations
4. **Document** - Session summary for continuity

**Estimated time:** 15-45 minutes

---

## Context Prompts

### Security Topic

**Question:** "What security topic do you need guidance on?"

**Options:**
- **Incident Response** - Playbooks, tabletop exercises, NIST 800-61
- **Access Control** - IAM, privilege management, authentication
- **Cloud Security** - AWS/Azure/GCP hardening, misconfigurations
- **Container Security** - Docker, Kubernetes, CIS benchmarks
- **Third-Party Risk** - Vendor assessment, supply chain, SaaS security
- **Security Program** - Building/improving security programs, metrics
- **Compliance** - HIPAA, PCI DSS, SOC 2, GDPR requirements
- **Application Security** - OWASP, secure coding, API security
- **Describe Custom Topic** - Provide specific question

**Default:** Describe Custom Topic

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Skill: security-advisory
Mode: ad-hoc-guidance

Topic: {user-selected-topic}
Question: {user-question}

CRITICAL - LIBRARY EXPLORATION:
┌─────────────────────────────────────────────────────────────────┐
│ BEFORE providing guidance, explore resources/library/ for      │
│ relevant context based on the user's topic:                    │
│                                                                 │
│ resources/library/                                              │
│ ├── benchmarks/     (CIS controls, hardening guides)           │
│ ├── books/          (security methodology books)               │
│ ├── frameworks/     (NIST, OWASP, PCI-DSS, HIPAA, GDPR, etc.) │
│ ├── methodologies/  (testing and assessment approaches)        │
│ ├── repositories/   (OWASP cheatsheets, ASVS, WSTG, etc.)     │
│ └── threat-intelligence/ (threat data and research)           │
│                                                                 │
│ Use Glob/Read to find and load relevant materials.             │
│ Cite specific framework sections in your response.             │
└─────────────────────────────────────────────────────────────────┘

Instructions:
1. Understand the specific question and context
2. Explore resources/library/ for relevant frameworks/standards
3. Provide framework-based guidance with citations
4. Include practical implementation steps
5. Note any caveats or organization-specific considerations
`
})
```

---

## Response Structure

```markdown
## Topic: {Security Topic}

### Question
{Restated user question}

### Framework Reference
- Primary: {NIST SP 800-X / CIS Control X / OWASP X}
- Supporting: {Additional relevant standards}

### Guidance

{Numbered best practices with citations}

1. **{Practice}** - {Description}
   - Reference: {Framework section}

### Implementation Steps

{Practical steps to implement}

### Considerations

{Organization-specific caveats, tradeoffs}

### References
- {Framework name and section}
- {Additional resources}
```

---

## Examples

### Container Security

```
/security-advice
→ Topic: Container Security
→ Question: How do I secure Docker containers in production?

Result: CIS Docker Benchmark guidance, image scanning recommendations,
        runtime security controls, Kubernetes pod security policies
```

### Incident Response

```
/security-advice
→ Topic: Incident Response
→ Question: What should our IR playbook include?

Result: NIST 800-61r3 phases, playbook structure, communication templates,
        lessons learned process
```

### API Security

```
/security-advice
→ Topic: Application Security
→ Question: Best practices for securing REST APIs?

Result: OWASP API Security Top 10, authentication patterns,
        rate limiting, input validation, logging requirements
```

---

## Related Commands

- `/risk-assessment` - Formal 22-question security assessment with deliverables
- `/arch-review` - Architecture threat modeling (STRIDE/PASTA)
- `/secure-config` - Infrastructure hardening validation
- `/code-review` - Security-focused code review

---

## References

**Library Resources:**
- `resources/library/frameworks/` - NIST, OWASP, PCI-DSS, HIPAA, GDPR
- `resources/library/repositories/` - OWASP cheatsheets, ASVS, WSTG
- `resources/library/benchmarks/` - CIS Controls

**External:**
- NIST Cybersecurity Framework: nist.gov/cyberframework
- OWASP: owasp.org
- CIS Controls: cisecurity.org/controls

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
