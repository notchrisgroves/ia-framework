---
name: code-review
description: Security-focused code analysis with dynamic language-specific vulnerability detection using WHAT/WHY/HOW methodology. Identifies OWASP Top 10/CWE Top 25 vulnerabilities with CWE classification and CVSS scoring. Use for SQL injection, XSS, authentication flaws, and secure coding validation.
---

# Code Review Skill

**Auto-loaded when `security` agent invoked for code security analysis**

Specialized in OWASP Top 10/CWE Top 25 vulnerability detection with language-specific root cause analysis (WHY vulnerabilities exist in each language, HOW to prevent them properly).

**Core Philosophy:** Dynamic language-specific standards lookup required (never static checklists). WHAT/WHY/HOW analysis mandatory for all findings. CWE classification and CVSS scoring ensure industry-standard reporting.

---

## 🚀 Quick Access

**Slash Command:** `/code-review`

Security-focused code review with dynamic language-specific vulnerability detection.

**See:** `commands/code-review.md` for complete workflow

---

## 🚨 Critical Rules

**Before starting any code review:**

1. **Load Context First** - Read CLAUDE.md → SKILL.md
2. **Dynamic Language-Specific Standards** - NEVER apply generic security checklist. ALWAYS dynamically look up current security standards for each specific language + version using WebSearch (ensures current 2025 standards, not outdated checklists)
3. **WHAT/WHY/HOW for Every Finding** - All vulnerability findings MUST include WHAT (description), WHY (root cause in this language), HOW (secure code pattern with explanation), POC (proof-of-concept)
4. **CWE Classification + CVSS Scoring Required** - All findings MUST have CWE ID and CVSS v3.1 score (ensures industry-standard reporting)
5. **Checkpoint After Major Code Section** - Update session file after reviewing major sections (auth, data layer, API endpoints) with section status, vulnerabilities found (CWE IDs), files reviewed, severity ratings

**Refresh Trigger:** If conversation exceeds 3 hours OR after 5+ code sections reviewed, refresh rules.

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` - Hook auto-detects escalation triggers and injects guidance.

**Default:** Sonnet | **Novel/Complex:** Opus | **WHY Explanation:** Grok Code | **QA:** Grok | **Validation:** Haiku

---

## When to Use

✅ **Use code-review for:**
- SQL/NoSQL injection in queries
- XSS in output rendering
- Command injection in system calls
- Deserialization vulnerabilities (pickle, YAML, JSON with classes)
- Cryptographic weaknesses (MD5, weak RNG, ECB mode)
- Authentication/authorization flaws
- Language-specific vulnerabilities (Python pickle, JavaScript prototype pollution, Rust unsafe blocks)
- Secure coding standards validation (SEI CERT, OWASP ASVS)
- Pre-release security review

❌ **Don't use if:**
- System architecture security design → Use `/arch-review` (architecture-review skill)
- Dependency vulnerability scanning → Use `/dependency-audit` (dependency-audit skill)
- Infrastructure configuration hardening → Use `/secure-config` (secure-config skill)
- Active penetration testing → Use `/pentest` (security-testing skill)
- CVE research → Use `/threat-intel` (threat-intel skill)

**Decision Guide:** If you have SOURCE CODE and want to find SECURITY BUGS, use code-review. If reviewing ARCHITECTURE DESIGN, use architecture-review.

---

## Prerequisites

**For Code Review:**
- Source code repository access (GitHub, GitLab, Bitbucket)
- Ability to read code, search codebase
- Dependency manifests (package.json, requirements.txt, pom.xml, Cargo.toml, go.mod)
- Version information (language versions, framework versions)

**Optional (Helpful):**
- Architecture diagrams
- API specifications
- Previous security assessments
- Authentication/authorization documentation

---

## Workflow: EXPLORE → PLAN → CODE → COMMIT

**Total Duration:** 6-12 hours for comprehensive code review

### Phase 1: EXPLORE - Codebase Discovery (1-2 hours)

**Goal:** Identify languages/versions, map codebase structure, identify high-risk areas

**Actions:**
1. Identify languages and versions (dependency manifests, version indicators)
2. Map codebase structure (authentication, database queries, API endpoints, file operations)
3. Review existing security controls

**Deliverables:**
- `SCOPE.md` with codebase structure
- Languages identified with versions
- High-risk areas mapped

**Checkpoint:** Languages identified, high-risk areas mapped

**Load for this phase:**
```
Read skills/code-review/SKILL.md
# Focus on: Language identification, codebase mapping
```

---

### Phase 2: PLAN - Dynamic Standards Research (1-2 hours)

**Goal:** Dynamically research language-specific security standards

**Actions:**
1. For EACH language identified, use WebSearch to research current (2025) security standards
2. For EACH library/framework, use Context7 to verify correct API usage patterns
3. Document language-specific vulnerabilities (WHAT, WHY they exist in this language)
4. Create language-specific review checklist
5. Prioritize review areas (critical → high → medium → low)

**Research Tools:**
- **Context7:** Library/framework API verification (prevents flagging correct usage as vulnerabilities)
  - Example: `get_library_docs("tiangolo/fastapi", topic="security")` for FastAPI auth patterns
  - Example: `get_library_docs("psf/requests", topic="ssl")` for requests SSL verification
- **WebSearch:** Language security standards (OWASP, CWE patterns, SEI CERT)

**Example WebSearch Queries:**
```
Python 3.11 security vulnerabilities 2025
Django security best practices 2025
Node.js 18 security best practices 2025
Express.js security vulnerabilities 2025
Rust 1.75 security best practices 2025
```

**Example Context7 Lookups:**
```python
from servers.context7 import search_libraries, get_library_docs

# Find library ID for framework being reviewed
search_libraries("fastapi")  # → tiangolo/fastapi

# Get security-specific documentation
get_library_docs("tiangolo/fastapi", topic="authentication")
get_library_docs("pallets/flask", topic="security")
get_library_docs("vercel/next.js", topic="middleware")
```

**Why Context7 for Code Review:**
- Prevents false positives (flagging correct API usage as vulnerable)
- Verifies library best practices before suggesting fixes
- Ensures recommendations match current library versions

**Deliverables:**
- `01-analysis/language-standards-research.md`
- Language-specific checklists
- Prioritized review plan

**Checkpoint:** Standards researched, review checklist created

**Load for this phase:**
```
Read skills/code-review/reference/language-lookup-guide.md
# Focus on: Dynamic lookup methodology, query patterns, WHAT/WHY/HOW template
```

---

### Phase 3: CODE - Security Review with WHAT/WHY/HOW (3-6 hours)

**Goal:** Conduct security review with WHAT/WHY/HOW analysis for each finding

**WHAT/WHY/HOW Template for Each Finding:**

**1. WHAT - Describe the Vulnerability**
```
Finding: SQL Injection in user search
File: app/controllers/users.py:42
Language: Python 3.11
CWE: CWE-89 (SQL Injection)
CVSS: 9.0 (Critical) - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
OWASP: A03:2021 - Injection
```

**2. WHY - Root Cause in This Language**
```
WHY VULNERABLE:
Python's f-strings directly interpolate user input into SQL strings
without escaping. The database cannot distinguish between SQL code
and data. Python's string formatting is designed for convenience,
not security - it doesn't understand SQL syntax.
```

**3. HOW - Show Vulnerable Code**
```python
# VULNERABLE
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**4. POC - Demonstrate Exploitability**
```python
# Attacker input
username = "admin' OR '1'='1"
# Results in: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# Returns all users (authentication bypass)
```

**5. HOW TO FIX - Secure Pattern**
```python
# SECURE
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**6. WHY FIX WORKS**
```
WHY IT'S SECURE:
Parameterized queries treat ? as data placeholders, not SQL code.
The database driver automatically escapes the input. Attacker cannot
inject SQL syntax because the query structure is fixed.
```

**Deliverables:**
- `02-findings/findings-register.md`
- `02-findings/poc-examples/`
- `03-threat-model/language-specific-threats.md`

**Checkpoint:** All sections reviewed, findings documented with WHAT/WHY/HOW

**Load for this phase:**
```
Read skills/code-review/methodologies/vulnerability-detection.md
# Focus on: OWASP Top 10, CWE Top 25, CVSS v3.1 scoring

Read skills/code-review/reference/language-[language].md
# Load language-specific guides as needed (Python, JavaScript, Rust, etc.)
```

---

### Phase 4: COMMIT - Reporting (1-2 hours)

**Goal:** Generate comprehensive report with language-specific analysis

**Quality Assurance - All findings must have:**
- ✅ WHAT description
- ✅ WHY root cause (language-specific)
- ✅ HOW to fix (secure code example)
- ✅ POC demonstrating exploitability
- ✅ CWE ID
- ✅ CVSS score
- ✅ References (OWASP, language-specific standards)

**Report Structure:**
1. Executive Summary
2. Language-Specific Analysis (separate section per language)
3. Findings with WHAT/WHY/HOW for each
4. Remediation Roadmap (prioritized by severity)
5. Standards References (dynamically researched URLs)

**Deliverables:**
- `04-reporting/security-code-review-report.md`
- `04-reporting/remediation-roadmap.md`
- `04-reporting/executive-summary.md`
- `COMPLETION-SUMMARY.md`

**Checkpoint:** All deliverables created, review complete

**Load for this phase:**
```
Read skills/code-review/templates/review-report.md
# Use as template for final deliverable
```

---

## Industry Standards

**Primary Frameworks:**
- **OWASP Top 10 (2021)** - Web application security risks (all web reviews)
- **CWE Top 25 (2023)** - Most dangerous software weaknesses (all reviews)
- **OWASP Code Review Guide v2.0** - Code review methodology
- **CVSS v3.1** - Common Vulnerability Scoring System (severity assessment)

**Language-Specific Standards:**
- **SEI CERT Coding Standards** - C, C++, Java, Android secure coding
- **NIST SP 800-218** - Secure Software Development Framework
- **OWASP ASVS** - Application Security Verification Standard

**Complete reference:** `reference/standards.md`

---

## Output Structure

```
output/engagements/code-reviews/{client}-{YYYY-MM}/
├── SCOPE.md
├── README.md
├── 01-analysis/
│   ├── language-standards-research.md
│   └── codebase-structure.md
├── 02-findings/
│   ├── findings-register.md
│   └── poc-examples/
├── 03-threat-model/
│   └── language-specific-threats.md
├── 04-reporting/
│   ├── security-code-review-report.md
│   ├── remediation-roadmap.md
│   └── executive-summary.md
└── COMPLETION-SUMMARY.md
```

**Multi-session tracking:** `sessions/YYYY-MM-DD-project-name.md`

---

## Progressive Context Loading

**Core Context (Always Loaded):**
- This SKILL.md file

**Extended Context (Load as Needed):**
- `methodologies/vulnerability-detection.md` - OWASP Top 10, CWE Top 25, CVSS v3.1 scoring
- `reference/standards.md` - OWASP Code Review Guide, SEI CERT, NIST SP 800-218, OWASP ASVS
- `reference/language-lookup-guide.md` - Dynamic lookup methodology, query patterns, WHAT/WHY/HOW template
- `reference/language-python.md` - Python-specific vulnerabilities with WHAT/WHY/HOW
- `reference/language-javascript.md` - JavaScript-specific vulnerabilities
- `reference/language-rust.md` - Rust-specific vulnerabilities (unsafe blocks, etc.)
- `workflows/security-code-review.md` - Complete 4-phase workflow with checkpoint system
- `templates/review-report.md` - Comprehensive security code review report template

**Create language guides as needed using dynamic lookup**

---

## Long-Session Rule Refresh

**Triggers:** Session > 3 hours OR 5+ code sections reviewed OR `/refresh-rules`

**Refresh statement:**
```
Refreshing critical rules for code review:
- Context loaded (CLAUDE.md + SKILL.md)
- Language-specific standards (dynamically researched for each language)
- WHAT/WHY/HOW analysis (root cause + secure patterns for all findings)
- CWE + CVSS required (industry-standard classifications)
- Checkpoints maintained (sections reviewed, vulnerabilities documented)
```

---

## Key Innovation: Dynamic Language-Specific Analysis

**Traditional Approach (Wrong):**
- Static security checklist
- Same rules for all languages
- Generic vulnerability descriptions

**This Skill's Approach (Right):**
1. **Identify** language + version
2. **Research** current security standards dynamically (WebSearch)
3. **Understand** WHY vulnerabilities exist in that language
4. **Apply** language-specific secure patterns
5. **Teach** WHAT/WHY/HOW for every finding

**Example - Same vulnerability class, different root causes:**

**Python Pickle Deserialization:**
- WHAT: pickle.loads(user_input) allows code execution
- WHY: pickle reconstructs Python objects including `__reduce__()` which can execute arbitrary code
- HOW: Use JSON for untrusted data (only deserializes data structures, no code execution)

**Rust Unsafe Blocks:**
- WHAT: Memory safety violations in unsafe code
- WHY: unsafe blocks bypass Rust's borrow checker for FFI/low-level operations
- HOW: Minimize unsafe scope, validate preconditions, wrap in safe API

---

## Common Mistakes to Avoid

**❌ Generic vulnerability descriptions without language context**
- Bad: "SQL injection found"
- Good: "SQL injection via Python f-string concatenation. Python's f-strings directly interpolate user input without escaping. Use parameterized queries instead."

**❌ Missing WHY (root cause) explanation**
- Must explain WHY vulnerability exists in THIS language
- What language feature/design enables it?

**❌ No POC/evidence**
- Every finding needs working exploit example
- Show HOW to exploit, not just THAT it's exploitable

**❌ Generic remediation**
- Bad: "Fix SQL injection"
- Good: [Show secure code with explanation of WHY it works in this language]

**❌ Static checklist for all languages**
- Don't check for buffer overflow in Python
- Don't check for prototype pollution in Rust
- Use dynamic standards lookup

**❌ Skipping dynamic research**
- Must use WebSearch to find current 2025 standards
- Don't rely on static 2019 checklists

---

## Quality Checks (Pre-Delivery)

**All code reviews must include:**
- ✅ Languages identified with versions
- ✅ Language-specific standards researched (WebSearch for 2025 standards)
- ✅ All findings have WHAT/WHY/HOW analysis
- ✅ All findings have POC demonstrating exploitability
- ✅ All findings have CWE ID and CVSS v3.1 score
- ✅ Language-specific root cause explanations (not generic)
- ✅ Secure code examples with WHY fix works
- ✅ Remediation roadmap prioritized by severity
- ✅ Standards references (OWASP, language-specific URLs)

---

**Version:** 2.1
**Last Updated:** 2025-12-19
**Model:** Claude Sonnet 4.5
**Framework:** OWASP Code Review Guide + Dynamic Language-Specific Standards
**Key Innovation:** WHAT/WHY/HOW analysis with dynamic standards lookup
**Research Tools:** Context7 (library APIs) + WebSearch (security standards)
