---
name: code-review
description: Security-focused code review for vulnerability detection
---

# /code-review - Security Code Review

Security-focused code analysis for vulnerability identification, secure coding standards validation, and threat modeling.

**Agent:** security
**Skill:** code-review
**Output:** `output/engagements/code-reviews/{project}-{YYYY-MM}/`

---

## Quick Start

```
/code-review
```

Collects code location → Performs security analysis → Generates vulnerability findings with remediation

---

## When to Use

✅ **Use /code-review when:**
- Identify security vulnerabilities in source code
- Validate secure coding practices (OWASP, CWE)
- Review code before production deployment
- Assess third-party or open-source code security
- Prepare for security audits or compliance reviews
- Train developers on secure coding patterns

❌ **Don't use if:**
- Need runtime vulnerability scanning → use `/vuln-scan`
- Need architecture-level review → use `/arch-review`
- Need dependency vulnerability analysis → use `/dependency-audit`

---

## Workflow

1. **Context Collection** - Prompts gather code location, language, review focus
2. **Analysis** - Static code analysis for security vulnerabilities
3. **Findings** - Categorize issues by severity, map to CWE/OWASP
4. **Output** - Generate review report in `output/engagements/code-reviews/{project}-{YYYY-MM}/`

**Estimated time:** 30-90 minutes

---

## Context Prompts

### Code Source

**Question:** "How will you provide the code to review?"

**Options:**
- **Directory Path** - Path to local codebase directory (recursive scan)
- **Specific Files** - List of specific file paths (targeted reviews)
- **Git Repository** - Clone from Git URL (public repos only)
- **Code Snippet** - Paste code directly (quick review)

**Default:** Directory Path

---

### Programming Language

**Question:** "What programming language(s) are you reviewing?"

**Options:**
- **Auto-Detect** - Agent detects languages from file extensions
- **JavaScript/TypeScript** - XSS, prototype pollution, injection
- **Python** - Injection, deserialization, insecure crypto
- **Java/C#** - Injection, XXE, deserialization
- **C/C++** - Buffer overflows, use-after-free, format strings
- **Go/Rust** - Concurrency, unsafe code, crypto misuse

**Multiple selection:** Yes

**Default:** Auto-Detect

---

### Review Depth

**Question:** "How thorough should the security review be?"

**Options:**
- **Quick Scan** - Automated static analysis (15-30 min), obvious vulnerabilities
- **Standard Review** - Balanced analysis with manual validation (45-60 min), OWASP Top 10
- **Deep Review** - Comprehensive manual review with threat modeling (90-120 min), logic flaws

**Default:** Standard Review

---

### Review Focus

**Question:** "What security areas should the review emphasize?"

**Options:**
- **OWASP Top 10** - Web application vulnerabilities (injection, broken auth, XSS)
- **CWE Top 25** - Most dangerous software weaknesses
- **Input Validation** - Injection flaws, sanitization, validation logic
- **Authentication/Authorization** - Access control, session management, privilege escalation
- **Cryptography** - Encryption, hashing, key management, random number generation
- **All Areas** - Comprehensive coverage (recommended)

**Multiple selection:** Yes

**Default:** OWASP Top 10

---

### Output Format

**Question:** "What output format do you need?"

**Options:**
- **Markdown Report** - Human-readable findings with code snippets, severity, remediation
- **SARIF** - Static Analysis Results Interchange Format (JSON) for tool integration
- **Both** - Generate both markdown and SARIF (recommended)

**Default:** Markdown Report

---

## Agent Routing

```typescript
// FLEXIBLE MODEL SELECTION (per library/model-selection-matrix.md):
//
// DEFAULT WORKFLOW: Sonnet executes, escalate strategically
//
// ULTRATHINK (Opus) - Strategic escalation points:
// ┌─────────────────────────────────────────────────────────────┐
// │ • Review methodology design for complex codebases           │
// │ • Novel vulnerability discovery (beyond OWASP/CWE)          │
// │ • Business logic flaw analysis                              │
// │ • When standard patterns don't explain the vulnerability    │
// └─────────────────────────────────────────────────────────────┘
//
// EXECUTION: Sonnet (pattern matching, OWASP/CWE detection, documentation)
// REASONING: Grok Code (WHY vulnerable - shows reasoning traces)
// QA/CHALLENGE: Grok (adversarial review - what did I miss?)
// VALIDATION: Haiku (format checks, quick syntax validation)

Task({
  subagent_type: "security",
  model: "sonnet",  // Default - escalate to opus/grok as needed
  prompt: `
Mode: code-review
Skill: code-review
Workflow: security-code-analysis

Context:
- Code Source: {directory|files|git-repo|snippet}
- Language: {auto|javascript|python|java|cpp|go|rust}
- Review Depth: {quick|standard|deep}
- Review Focus: {owasp|cwe|input-validation|auth|crypto|all}
- Output Format: {markdown|sarif|both}

FLEXIBLE MODEL ESCALATION:
┌─────────────────────────────────────────────────────────────────┐
│ ULTRATHINK (Opus) - Invoke for:                                 │
│ • Designing review approach for complex/unfamiliar codebases    │
│ • Novel vulnerability patterns (not in standard checklists)     │
│ • Business logic vulnerabilities (requires understanding flow)  │
│ • Multi-file attack chains (A calls B which enables C exploit)  │
│ • When stuck: "I found injection but something else is wrong"   │
├─────────────────────────────────────────────────────────────────┤
│ EXECUTION (Sonnet) - Default for:                               │
│ • Standard OWASP Top 10 / CWE Top 25 pattern matching           │
│ • Known vulnerability detection (injection, XSS, auth flaws)    │
│ • Documentation and finding write-ups                           │
│ • Remediation guidance for known issues                         │
├─────────────────────────────────────────────────────────────────┤
│ REASONING (Grok Code) - Escalate for:                           │
│ • "WHY is this vulnerable?" - shows reasoning traces            │
│ • Complex injection paths needing step-by-step explanation      │
│ • Educational reviews (training developers on WHY not just WHAT)│
│ • When you need to EXPLAIN the vulnerability to stakeholders    │
├─────────────────────────────────────────────────────────────────┤
│ QA/CHALLENGE (Grok) - Escalate for:                             │
│ • "What vulnerabilities did I miss?" adversarial review         │
│ • Second opinion on severity ratings                            │
│ • Challenge "this looks safe" assumptions                       │
├─────────────────────────────────────────────────────────────────┤
│ VALIDATION (Haiku) - Use for:                                   │
│ • Quick format/syntax checks                                    │
│ • SARIF output validation                                       │
│ • Checklist verification                                        │
└─────────────────────────────────────────────────────────────────┘

Instructions:
Execute code-review SKILL.md workflow:
1. Static code analysis for security vulnerabilities
2. Categorize issues by severity
3. Map to CWE/OWASP
4. Generate findings with remediation

Output: output/engagements/code-reviews/{project}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/engagements/code-reviews/{project}-{YYYY-MM}/
├── REVIEW-SUMMARY.md
├── FINDINGS.md
├── CODE-QUALITY.md
├── REMEDIATION-GUIDE.md
├── results/
│   ├── findings.sarif
│   ├── scan-logs/
│   └── code-snippets/
└── session-state.md
```

**Deliverables:**

1. **Review Summary** - Overall security posture, critical findings count, top 5 risks, compliance status

2. **Findings** - Vulnerability details with severity, CWE/OWASP mapping, affected code location, code snippet, exploitation scenario, remediation

3. **Code Quality Assessment** - Secure coding practices score, anti-patterns, best practices adherence

4. **Remediation Guide** - Prioritized fix list (P0/P1/P2), code examples, testing guidance, timeline estimate

5. **SARIF Output** (if requested) - Machine-readable findings, GitHub Security compatible, IDE ready

---

## Examples

### Web Application Review

```
/code-review
→ Source: Directory | Language: JavaScript/TypeScript | Depth: Standard

Result: OWASP Top 10 analysis (~45-60 min)
Output: output/engagements/code-reviews/webapp-2025-12/
```

### Quick PR Scan (CI/CD)

```
/code-review
→ Source: Specific Files (5 changed) | Language: Python | Depth: Quick

Result: Fast security scan for PR checks (~10-15 min)
Output: SARIF format for automated pipeline
```

---

## Security Considerations

**Code Privacy:**
- Code stays local (not sent externally without permission)
- Sanitize findings before sharing
- Consider NDA and confidentiality requirements
- Use local-only tools for sensitive codebases

**Finding Disclosure:**
- Do not publish findings publicly without permission
- Follow coordinated disclosure timelines
- Report critical findings immediately
- Document remediation before public disclosure

**Tool Limitations:**
- Cannot detect all vulnerability classes
- May miss business logic flaws
- Runtime behavior not analyzed
- Complement with dynamic testing

---

## Related Commands

- `/arch-review` - Architecture-level security review
- `/dependency-audit` - Third-party dependency vulnerability analysis
- `/vuln-scan` - Runtime vulnerability scanning
- `/pentest` - Penetration testing with exploitation

---

## References

**Frameworks:**
- OWASP Top 10: owasp.org/www-project-top-ten
- CWE Top 25: cwe.mitre.org/top25
- SARIF: docs.oasis-open.org/sarif

**Secure Coding Guidelines:**
- OWASP Secure Coding Practices
- CERT Secure Coding Standards
- Language-specific security guides

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
