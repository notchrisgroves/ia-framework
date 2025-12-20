---
type: workflow
name: security-code-review
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Security Code Review Workflow

**Complete 4-phase workflow for security-focused code reviews**

This document covers the end-to-end process for conducting security code reviews with dynamic language-specific lookup.

---

## Workflow Overview

**Total Time:** 6-12 hours for comprehensive code review (depends on codebase size)

**4 Phases:**
1. **EXPLORE** (1-2 hours) - Understand codebase, identify languages, gather context
2. **PLAN** (1-2 hours) - Dynamic lookup of language-specific standards, prioritize review areas
3. **CODE** (3-6 hours) - Conduct security review with language-specific lens
4. **COMMIT** (1-2 hours) - Generate findings report, remediation guidance

**Output:** Security code review report with vulnerability findings, POC examples, remediation guidance

---

## Prerequisites

### Required Materials

**Source Code Access:**
- Repository access (GitHub, GitLab, Bitbucket)
- Ability to read code, search codebase
- Version control history (for context)

**Context Documentation:**
- Architecture diagrams (if available)
- API specifications (OpenAPI/Swagger)
- Dependency manifests (package.json, requirements.txt, pom.xml, etc.)
- Previous security assessments (if available)

**Business Context:**
- Application purpose and functionality
- Sensitivity of data processed
- Compliance requirements (PCI DSS, HIPAA, etc.)
- Authentication/authorization model

---

## Phase 1: EXPLORE (1-2 hours)

**Objective:** Understand codebase structure, identify languages, gather security-relevant context

### Step 1.1: Load Framework Context (5 min)

**Actions:**
```
Read CLAUDE.md
Read skills/code-review/SKILL.md
```

**Checkpoint:** Context loaded

---

### Step 1.2: Identify Languages and Versions (15 min)

**Look for version indicators:**

**Python:**
```python
# pyproject.toml, setup.py, requirements.txt
python_requires = ">=3.11"
```

**JavaScript/Node.js:**
```json
// package.json
"engines": {
  "node": ">=18.0.0"
}
```

**Java:**
```xml
<!-- pom.xml -->
<maven.compiler.source>17</maven.compiler.source>
```

**Rust:**
```toml
# Cargo.toml
rust-version = "1.75"
```

**Go:**
```go
// go.mod
go 1.21
```

**C#:**
```xml
<!-- .csproj -->
<TargetFramework>net8.0</TargetFramework>
```

**Actions:**
1. Check dependency manifest files
2. Look for version-specific syntax (type hints in Python 3.5+, pattern matching in C# 9+)
3. Identify frameworks (Django, Flask, Spring Boot, ASP.NET, Rails, Express)

**Checkpoint:** Document languages, versions, frameworks in notes

---

### Step 1.3: Map Codebase Structure (30 min)

**Identify key code sections:**

**Authentication/Authorization:**
- Login/logout endpoints
- Session management
- Password hashing
- Token generation/validation
- Permission checks

**Data Access Layer:**
- Database queries
- ORM usage
- SQL string construction
- NoSQL operations

**API Endpoints:**
- Input validation
- Output encoding
- Rate limiting
- Error handling

**File Operations:**
- File uploads
- File path handling
- File downloads
- Temp file management

**External Integrations:**
- HTTP requests to external APIs
- Command execution
- Third-party library usage

**Cryptography:**
- Encryption/decryption
- Hashing
- Random number generation
- Key management

**Actions:**
1. Use Glob/Grep to find authentication-related code
2. Map database access patterns
3. Identify all API endpoints
4. Locate file operation code
5. Find cryptography usage

**Checkpoint:** Codebase structure mapped, high-risk areas identified

---

### Step 1.4: Review Existing Security Controls (20 min)

**Check for:**
- Input validation libraries (validator.js, Joi, etc.)
- CSRF protection (enabled/disabled)
- Security headers middleware (helmet, etc.)
- Rate limiting implementation
- Logging/monitoring setup
- Authentication libraries (Passport, Spring Security, etc.)

**Actions:**
1. Search for security middleware in framework setup
2. Check if HTTPS is enforced
3. Verify security headers configuration
4. Look for rate limiting on authentication endpoints

**Checkpoint:** Existing security controls documented

---

### 🔒 CHECKPOINT: Phase 1 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 1: EXPLORE - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Languages Identified:**
- [Language 1]: [Version]
- [Language 2]: [Version]

**Frameworks:**
- [Framework 1]: [Version]

**High-Risk Areas:**
- Authentication: [file paths]
- Data Access: [file paths]
- API Endpoints: [file paths]
- File Operations: [file paths]
- Cryptography: [file paths]

**Existing Security Controls:**
- [Control 1]: [Status]
- [Control 2]: [Status]

**Next Action:** Phase 2 - PLAN (Dynamic standards lookup)
```

---

## Phase 2: PLAN (1-2 hours)

**Objective:** Dynamically look up language-specific security standards and plan review approach

### Step 2.1: Dynamic Standards Lookup (30-45 min)

**For EACH language identified:**

**Load:** `reference/language-lookup-guide.md`

**WebSearch for current standards:**

**Python 3.11:**
```
WebSearch: "Python 3.11 security vulnerabilities"
WebSearch: "Django 4.2 security best practices"
WebSearch: "Flask security vulnerabilities"
```

**JavaScript/Node.js 18:**
```
WebSearch: "Node.js 18 security best practices"
WebSearch: "Express.js security vulnerabilities"
WebSearch: "React XSS prevention 2025"
```

**Java 17:**
```
WebSearch: "Java 17 security best practices"
WebSearch: "Spring Boot security vulnerabilities"
WebSearch: "Java deserialization attacks 2025"
```

**For each language, create notes:**
```markdown
## [Language] [Version] Security Standards

**Primary Vulnerabilities:**
1. [Vuln 1] - WHAT, WHY, HOW to prevent
2. [Vuln 2] - WHAT, WHY, HOW to prevent
3. [Vuln 3] - WHAT, WHY, HOW to prevent

**Language-Specific Libraries:**
- [Secure library 1] for [purpose]
- [Secure library 2] for [purpose]

**Key Resources:**
- [URL 1]: [Description]
- [URL 2]: [Description]
```

**Checkpoint:** Language-specific standards documented

---

### Step 2.2: Prioritize Review Areas (15 min)

**Risk-Based Prioritization:**

**Critical (Review First):**
- Authentication/authorization code
- SQL/NoSQL query construction
- Deserialization of untrusted data
- Command execution with user input
- Password hashing implementation
- File upload handling

**High (Review Second):**
- Input validation on API endpoints
- Output encoding for XSS prevention
- Session management
- Cryptographic operations
- Error handling and logging

**Medium (Review Third):**
- Rate limiting implementation
- CSRF protection
- Security headers configuration
- Dependency versions

**Checkpoint:** Review priorities set

---

### Step 2.3: Define Review Checklist (30 min)

**Create language-specific checklist:**

**Example for Python/Django:**
```markdown
### Authentication Review
- [ ] Password hashing uses bcrypt/argon2 (not MD5/SHA1)
- [ ] MFA implementation reviewed
- [ ] Session regeneration after login
- [ ] Account lockout after failed attempts

### SQL Injection Prevention
- [ ] No f-strings or .format() in queries
- [ ] ORM used correctly (no .raw() with user input)
- [ ] All database operations use parameterized queries

### Deserialization
- [ ] No pickle.loads() with untrusted data
- [ ] JSON used for external data
- [ ] YAML uses safe_load() not load()

### Command Injection
- [ ] No os.system() with user input
- [ ] subprocess uses list args (not shell=True)
- [ ] Input validation on all shell commands

### Path Traversal
- [ ] File paths validated with os.path.abspath()
- [ ] startswith() check for allowed directories
- [ ] No direct use of user input in open()

### Cryptography
- [ ] secrets module used (not random) for tokens
- [ ] TLS 1.2+ enforced
- [ ] No hardcoded secrets in code

### Django-Specific
- [ ] DEBUG = False in production
- [ ] CSRF protection enabled
- [ ] Security middleware active
```

**Checkpoint:** Language-specific checklist created

---

### 🔒 CHECKPOINT: Phase 2 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 2: PLAN - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Language-Specific Standards Researched:**
- [Language 1]: [Standards URLs]
- [Language 2]: [Standards URLs]

**Review Priorities:**
1. Critical: [Areas]
2. High: [Areas]
3. Medium: [Areas]

**Review Checklist Created:**
- [X] items for [Language 1]
- [Y] items for [Language 2]

**Next Action:** Phase 3 - CODE (Conduct security review)
```

---

## Phase 3: CODE (3-6 hours)

**Objective:** Conduct security code review with language-specific vulnerability analysis

### Step 3.1: Review Critical Areas (2-3 hours)

**For EACH critical area, follow WHAT/WHY/HOW pattern:**

#### Authentication Review Example

**Find authentication code:**
```bash
grep -r "password" --include="*.py" | grep -E "(hash|bcrypt|md5)"
```

**Analyze each finding:**

**Finding 1: Password Hashing**
```python
# File: app/auth.py:42
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Analysis:**
- **WHAT:** MD5 used for password hashing
- **WHY VULNERABLE:** MD5 is too fast (~1 billion hashes/sec on GPU), no salt → rainbow tables effective
- **CWE:** CWE-327 (Broken Crypto), CWE-916 (Weak Password Hashing)
- **CVSS:** 7.5 (High) - AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N

**Proof-of-Concept:**
```python
# Attacker can crack MD5 hashes quickly
import hashlib
# Try common passwords
passwords = ['password', '123456', 'admin123']
target_hash = 'e10adc3949ba59abbe56e057f20f883e'  # MD5('123456')
for pwd in passwords:
    if hashlib.md5(pwd.encode()).hexdigest() == target_hash:
        print(f"Cracked: {pwd}")  # Found in milliseconds
```

**Remediation:**
```python
# app/auth.py:42
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

**WHY REMEDIATION WORKS:**
- bcrypt is intentionally slow (~100ms per hash) → GPU-resistant
- Automatic salt → rainbow tables ineffective
- Adjustable work factor → future-proof

**Document Finding:**
```markdown
### F-001: Weak Password Hashing (MD5)

**Severity:** High (CVSS 7.5)
**CWE:** CWE-327, CWE-916
**Location:** app/auth.py:42

**Vulnerable Code:**
[code snippet]

**Impact:**
Attacker can crack user passwords using rainbow tables or brute force.

**Proof-of-Concept:**
[POC code]

**Remediation:**
[secure code]

**References:**
- OWASP Password Storage Cheat Sheet
- NIST SP 800-63B (Password Guidelines)
```

**Checkpoint:** Finding documented with WHAT/WHY/HOW/POC/Remediation

---

### Step 3.2: Review High Priority Areas (1-2 hours)

**Continue same WHAT/WHY/HOW pattern for:**
- Input validation
- Output encoding
- Session management
- Cryptographic operations

**For each vulnerability found:**
1. **WHAT:** Describe the vulnerability
2. **WHY:** Explain root cause in this language
3. **HOW:** Provide secure code example
4. **POC:** Demonstrate exploitability
5. **CWE:** Map to CWE ID
6. **CVSS:** Calculate severity score

**Checkpoint:** High priority areas reviewed, findings documented

---

### Step 3.3: Review Medium Priority Areas (1 hour)

**Quick review of:**
- Rate limiting
- CSRF protection
- Security headers
- Dependency versions

**Use automated tools if available:**
```bash
# Python
bandit -r . -f json -o bandit-report.json
safety check

# JavaScript
npm audit
snyk test

# Java
mvn dependency:tree
./mvnw org.owasp:dependency-check-maven:check
```

**Checkpoint:** Medium priority areas reviewed

---

### Step 3.4: Language-Specific Deep Dive (1-2 hours)

**Focus on language-specific vulnerabilities:**

**Python:**
- Search for `pickle.loads`, `yaml.load`, `eval`, `exec`
- Check for `os.system`, `subprocess` with `shell=True`
- Verify `secrets` used instead of `random`

**JavaScript:**
- Search for `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`
- Check `child_process.exec` usage
- Look for prototype pollution (`__proto__`)

**Java:**
- Search for `ObjectInputStream`, `readObject`
- Check XML parser configuration (XXE)
- Verify `PreparedStatement` usage (not string concatenation)

**Checkpoint:** Language-specific vulnerabilities reviewed

---

### 🔒 CHECKPOINT: Phase 3 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 3: CODE - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Areas Reviewed:**
- Authentication: COMPLETE
- Data Access: COMPLETE
- API Endpoints: COMPLETE
- File Operations: COMPLETE
- Cryptography: COMPLETE

**Findings Summary:**
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]
- Total: [N]

**Files Created:**
- `02-findings/findings-register.md`
- `02-findings/poc-examples/`

**Next Action:** Phase 4 - COMMIT (Generate report)
```

---

## Phase 4: COMMIT (1-2 hours)

**Objective:** Generate comprehensive security code review report with findings and remediation

### Step 4.1: Quality Assurance (15 min)

**Validation checklist:**
- [ ] All findings have CWE IDs
- [ ] All findings have CVSS scores
- [ ] All findings have POC/code examples
- [ ] All findings have remediation guidance
- [ ] All findings reference OWASP/CWE standards
- [ ] Language-specific standards applied correctly
- [ ] No generic/theoretical findings without evidence

**Review findings for:**
- False positives (verify exploitability)
- Missing context (add business impact)
- Duplicate findings (consolidate)

**Checkpoint:** Findings validated

---

### Step 4.2: Generate Findings Report (30 min)

**Use template:** `templates/review-report.md`

**Report Structure:**
1. Executive Summary
2. Scope and Methodology
3. Findings by Severity
4. Language-Specific Analysis
5. Remediation Roadmap
6. References

**For each finding, include:**
- Finding ID, Title, Severity, CWE
- Location (file:line)
- Vulnerable code snippet
- Root cause explanation (WHY in this language)
- Proof-of-concept
- Secure code example (HOW to fix)
- CVSS score breakdown
- References (OWASP, CWE, language-specific standards)

**Checkpoint:** Findings report generated

---

### Step 4.3: Create Remediation Roadmap (20 min)

**Prioritize findings:**

**Critical (Immediate - 0-7 days):**
- Deserialization vulnerabilities
- SQL injection
- Command injection
- Hardcoded credentials

**High (Urgent - 7-30 days):**
- Weak password hashing
- Missing authentication checks
- XSS vulnerabilities
- Path traversal

**Medium (Planned - 30-90 days):**
- Missing rate limiting
- Weak session configuration
- Information disclosure

**Low (Informational - When resources available):**
- Missing security headers
- Outdated dependencies (no known exploits)
- Code quality issues

**For each priority level:**
- Estimated remediation effort (hours/days)
- Impact if not fixed (business risk)
- Recommended owner (dev team, security team, etc.)

**Checkpoint:** Remediation roadmap created

---

### Step 4.4: Generate Executive Summary (15 min)

**High-level summary for stakeholders:**
- Application reviewed
- Review methodology (OWASP Code Review Guide + language-specific standards)
- Security posture (Strong / Adequate / Weak)
- Total findings by severity
- Top 3-5 critical issues
- Recommended actions

**Checkpoint:** Executive summary written

---

### Step 4.5: Create Completion Summary (10 min)

**File:** `COMPLETION-SUMMARY.md`

**Contents:**
- Review completion date
- Total vulnerabilities found (by severity)
- Key findings (top 3-5)
- Languages reviewed with specific standards applied
- Remediation effort estimates
- Next steps (implementation, re-review timeline)

**Checkpoint:** Completion summary created

---

### 🔒 CHECKPOINT: Phase 4 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 4: COMMIT - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Deliverables Created:**
- Security code review report (complete)
- Findings register (N findings)
- Remediation roadmap (prioritized)
- Executive summary
- Completion summary

**Files Created:**
- `04-reporting/security-code-review-report.md`
- `04-reporting/remediation-roadmap.md`
- `04-reporting/executive-summary.md`
- `COMPLETION-SUMMARY.md`

**Next Action:** N/A - Code review complete
```

---

## Final Deliverables

**Required outputs:**
1. **Findings Register** - All vulnerabilities with CWE, CVSS, POC, remediation
2. **Security Code Review Report** - Complete analysis with language-specific context
3. **Remediation Roadmap** - Prioritized fixes with effort estimates
4. **Executive Summary** - High-level overview for stakeholders
5. **POC Examples** - Working exploit code (when safe to include)

**Output Directory:**
```
output/engagements/code-reviews/[client]-[YYYY-MM]/
   SCOPE.md
   README.md
   # Multi-session tracking in `sessions/
   01-analysis/
      language-standards-research.md
      codebase-structure.md
   02-findings/
      findings-register.md
      poc-examples/
   03-threat-model/
      language-specific-threats.md
   04-reporting/
      security-code-review-report.md
      remediation-roadmap.md
      executive-summary.md
   COMPLETION-SUMMARY.md
```

---

## Common Mistakes to Avoid

**❌ Generic findings without language context**
- Bad: "SQL injection vulnerability found"
- Good: "SQL injection via Python f-string concatenation (app/db.py:42). Python's f-strings directly interpolate user input into SQL without escaping. Use parameterized queries instead."

**❌ Missing POC/evidence**
- Must include vulnerable code + exploit example
- Show HOW to exploit, not just THAT it's exploitable

**❌ No root cause explanation**
- Explain WHY vulnerability exists in THIS language
- What language feature enables it?

**❌ Generic remediation**
- Bad: "Fix the SQL injection"
- Good: [Show secure code example with explanation of WHY it works]

**❌ Static checklist for all languages**
- Don't apply buffer overflow checks to Python
- Don't check for prototype pollution in Rust
- Use language-specific standards dynamically

**❌ No checkpoints for long reviews**
- Update session file after each phase
- Essential for 6-12 hour reviews

---

## Time Estimates

| Phase | Standard Review | Comprehensive Review |
|---|---|---|
| **Phase 1: EXPLORE** | 1 hour | 2 hours |
| **Phase 2: PLAN** | 1 hour | 2 hours |
| **Phase 3: CODE** | 3 hours | 6 hours |
| **Phase 4: COMMIT** | 1 hour | 2 hours |
| **Total** | **6 hours** | **12 hours** |

**Factors affecting time:**
- Codebase size (LOC, number of files)
- Number of languages (each requires separate standards lookup)
- Code complexity (microservices vs monolith)
- Existing security controls (more controls = less time)
- Framework familiarity (known framework = faster)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Framework:** OWASP Code Review Guide + Dynamic Language-Specific Standards
**Key Innovation:** WHAT/WHY/HOW analysis for every finding
