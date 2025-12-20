# Security Reports Workflow

**Professional security assessment reports following industry standards**

**Standards:** PTES, OWASP, NIST 800-115

---

## Report Types

| Type | Standard | Use Case | Template |
|------|----------|----------|----------|
| **Penetration Test** | PTES | External/internal pentests | `PENTEST-REPORT-TEMPLATE.md` |
| **Web Application** | OWASP | Web app security assessments | `WEB-APP-REPORT-TEMPLATE.md` |
| **Infrastructure** | NIST 800-115 | Server/network audits | `PENTEST-REPORT-TEMPLATE.md` |
| **Bug Bounty** | Platform-specific | H1/Bugcrowd submissions | `BUG-BOUNTY-REPORT-TEMPLATE.md` |

---

## Workflow Overview

1. **GATHER** - Collect findings from engagement
2. **STRUCTURE** - Organize by severity and category
3. **WRITE** - Executive summary + technical findings
4. **EVIDENCE** - Screenshots, proof-of-concept, logs
5. **REMEDIATION** - Actionable fix guidance
6. **REVIEW** - Technical accuracy validation
7. **DELIVER** - Professional PDF + supporting files

---

## Stage 1: GATHER FINDINGS

### Source Materials

**Engagement artifacts:**
- Findings log: `output/engagements/[type]/[id]/02-findings/findings.md`
- Screenshots: `output/engagements/[type]/[id]/02-findings/evidence/`
- Scan results: `output/engagements/[type]/[id]/01-reconnaissance/scans/`
- Exploitation notes: `output/engagements/[type]/[id]/03-exploitation/notes.md`

**Read complete engagement:**
```bash
# Findings
Read(file_path="output/engagements/pentest/[id]/02-findings/findings.md")

# Evidence
Glob(pattern="output/engagements/pentest/[id]/02-findings/evidence/*")

# Session notes
Read(file_path="sessions/YYYY-MM-DD-pentest-[client].md")
```

### Findings Inventory

**Create findings inventory:**
```markdown
# Findings Inventory

## Critical (9.0-10.0 CVSS)
1. [Finding title] - [CVSS score]
   - Location: [URL/system/component]
   - Impact: [Business impact]
   - Evidence: [Screenshot/log reference]

## High (7.0-8.9 CVSS)
...

## Medium (4.0-6.9 CVSS)
...

## Low (0.1-3.9 CVSS)
...

## Informational
...
```

---

## Stage 2: STRUCTURE REPORT

### Template Selection

**Choose template based on report type:**
- Pentest: `skills/security-testing/templates/PENTEST-REPORT-TEMPLATE.md`
- Bug Bounty: `skills/security-testing/templates/BUG-BOUNTY-SUBMISSION-TEMPLATE.md`

**Copy template to engagement:**
```bash
cp skills/security-testing/templates/PENTEST-REPORT-TEMPLATE.md \
   output/engagements/pentest/[id]/04-reporting/report.md
```

### Report Structure (PTES Standard)

**Sections (in order):**
1. Executive Summary (1-2 pages, non-technical)
2. Assessment Overview (scope, methodology, timeline)
3. Findings Summary (severity breakdown, statistics)
4. Technical Findings (detailed, evidence-based)
5. Remediation Roadmap (prioritized fixes)
6. Appendices (methodology details, tools used)

---

## Stage 3: WRITE REPORT

### Executive Summary

**Audience:** C-level, decision-makers (non-technical)

**Content:**
- What was tested (scope in business terms)
- What was found (severity overview, counts)
- Business impact (risk to organization)
- Recommended actions (prioritized next steps)

**Tone:** Professional, clear, no jargon

**Length:** 1-2 pages maximum

**Example:**
```markdown
## Executive Summary

Intelligence Adjacent conducted a penetration test of Acme Corporation's
external attack surface from November 15-22, 2025. The assessment identified
12 vulnerabilities across web applications, infrastructure, and cloud services.

**Critical Findings:** 2 vulnerabilities allow unauthorized access to customer data
**High Findings:** 4 vulnerabilities enable privilege escalation
**Medium/Low:** 6 vulnerabilities present limited risk

**Immediate Actions Required:**
1. Patch SQL injection in customer portal (CRITICAL)
2. Implement multi-factor authentication (HIGH)
3. Update TLS configuration (MEDIUM)

Detailed findings and remediation guidance follow in this report.
```

### Technical Findings

**For EACH finding:**

**1. Title** (descriptive, specific)
```markdown
### SQL Injection in Customer Portal Login
```

**2. Severity** (CVSS 3.1 with justification)
```markdown
**Severity:** Critical (CVSS 9.8)
**Vector:** AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```

**3. Location** (where vulnerability exists)
```markdown
**Location:** https://portal.acme.com/login
**Component:** Customer authentication API endpoint
**Parameters:** username, password
```

**4. Description** (what the vulnerability is)
```markdown
**Description:** The login endpoint does not properly sanitize user input,
allowing SQL injection via the username parameter. An attacker can inject
SQL commands to bypass authentication or extract database contents.
```

**5. Impact** (business/technical consequences)
```markdown
**Impact:**
- Unauthorized access to customer accounts
- Full database extraction (PII, credentials)
- Data manipulation or deletion
- Compliance violations (GDPR, CCPA)
```

**6. Evidence** (proof the vulnerability exists)
```markdown
**Evidence:**

Request:
\`\`\`http
POST /api/login HTTP/1.1
Host: portal.acme.com
Content-Type: application/json

{"username": "admin' OR '1'='1", "password": "any"}
\`\`\`

Response:
\`\`\`json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {"id": 1, "role": "admin"}
}
\`\`\`

![SQL Injection Proof](evidence/sql-injection-admin-bypass.png)
```

**7. Remediation** (how to fix, actionable steps)
```markdown
**Remediation:**

**Immediate (within 24 hours):**
1. Disable affected endpoint until patched
2. Review access logs for exploitation attempts
3. Notify security team and stakeholders

**Short-term (within 1 week):**
1. Implement parameterized queries:
   \`\`\`python
   # Bad (vulnerable)
   query = f"SELECT * FROM users WHERE username = '{username}'"

   # Good (secure)
   query = "SELECT * FROM users WHERE username = ?"
   cursor.execute(query, (username,))
   \`\`\`
2. Add input validation (whitelist allowed characters)
3. Implement rate limiting on authentication endpoints

**Long-term:**
1. Security code review of all authentication flows
2. Implement Web Application Firewall (WAF)
3. Regular penetration testing (quarterly)
```

**8. References** (CVE, CWE, resources)
```markdown
**References:**
- CWE-89: SQL Injection
- OWASP Top 10 2021: A03 - Injection
- MITRE ATT&CK: T1190 - Exploit Public-Facing Application
```

---

## Stage 4: EVIDENCE MANAGEMENT

### Evidence Organization

```
output/engagements/pentest/[id]/04-reporting/evidence/
├── screenshots/
│   ├── 01-sql-injection-admin-bypass.png
│   ├── 02-rce-command-execution.png
│   └── 03-sensitive-data-exposure.png
├── logs/
│   ├── burp-requests.txt
│   ├── nmap-scan-results.xml
│   └── exploitation-session.log
└── poc/
    ├── sql-injection-poc.py
    ├── rce-exploit.sh
    └── README.md
```

### Screenshot Standards

**Requirements:**
- Clear, readable, annotated
- Shows vulnerability exploitation
- Includes timestamp/URL in view
- Redact sensitive data (PII, real credentials)

**Tools:**
- Burp Suite screenshots
- Browser DevTools Network tab
- Terminal output with timestamps

### Proof-of-Concept Code

**Include when:**
- Complex exploitation requiring steps
- Demonstrating automated exploit
- Helping client reproduce finding

**Standards:**
- Commented, explained
- Safe to run (no destructive actions by default)
- Includes usage instructions

---

## Stage 5: REMEDIATION ROADMAP

### Prioritization Matrix

| Severity | Ease of Fix | Priority | Timeframe |
|----------|-------------|----------|-----------|
| Critical | Any | P0 | 24-48 hours |
| High | Easy | P1 | 1 week |
| High | Hard | P2 | 2 weeks |
| Medium | Easy | P3 | 1 month |
| Medium | Hard | P4 | 2 months |
| Low | Any | P5 | 3 months |

### Roadmap Structure

```markdown
## Remediation Roadmap

### Phase 1: Critical Response (24-48 hours)
**Goal:** Eliminate critical risk

1. SQL Injection (Finding 1)
   - Action: Disable endpoint, implement parameterized queries
   - Owner: Development Team
   - Validation: Re-test after patch

2. Remote Code Execution (Finding 2)
   - Action: Update vulnerable library, restrict access
   - Owner: Infrastructure Team
   - Validation: Version verification

### Phase 2: High-Priority Fixes (1-2 weeks)
...

### Phase 3: Long-Term Improvements (1-3 months)
...
```

---

## Stage 6: REVIEW & VALIDATION

### Technical Accuracy Check

**Validate:**
- [ ] CVSS scores calculated correctly
- [ ] All findings reproducible (evidence valid)
- [ ] Remediation steps technically sound
- [ ] No false positives included
- [ ] Impact assessment accurate

### Quality Standards

**Report must:**
- [ ] Professional language (no slang, no ego)
- [ ] Evidence-based only (no speculation)
- [ ] Actionable remediation (specific steps)
- [ ] Complete coverage (all findings documented)
- [ ] Executive summary readable by non-technical

---

## Stage 7: DELIVER REPORT

### Deliverables Package

```
acme-pentest-2025-11.zip
├── PENTEST-REPORT-acme-2025-11.pdf           (Main report)
├── EXECUTIVE-SUMMARY-acme-2025-11.pdf        (Standalone exec summary)
├── REMEDIATION-TRACKER-acme-2025-11.xlsx     (Tracking spreadsheet)
├── evidence/
│   ├── screenshots/ (All PNGs)
│   ├── logs/ (Scan results, session logs)
│   └── poc/ (Proof-of-concept scripts)
└── README.txt (Package contents description)
```

### Report Formats

**PDF Generation:**
```bash
# Using Pandoc
pandoc report.md -o report.pdf \
  --toc \
  --number-sections \
  --highlight-style=tango \
  --pdf-engine=xelatex
```

**Standalone Executive Summary:**
- Extract executive summary section
- Separate PDF for leadership
- Include severity chart/graph

### Delivery Method

**Secure delivery:**
- Encrypted ZIP (AES-256)
- Password shared via separate channel
- Uploaded to secure client portal
- Physical media if required

---

## Report Type Specific Notes

### Bug Bounty Reports

**Platform-specific requirements:**
- H1: Use template, include impact video, CVSS score
- Bugcrowd: VRT category, clear reproduction steps
- Intigriti: Include remediation difficulty estimate

**Tone:** Professional but concise
**Evidence:** Video proof often required
**Timeline:** Report ASAP (race condition)

**Template:** `skills/security-testing/templates/BUG-BOUNTY-SUBMISSION-TEMPLATE.md`

### Compliance Reports

**Additional sections for compliance:**
- Compliance framework mapping (NIST, PCI-DSS, etc.)
- Control effectiveness ratings
- Compliance gap analysis
- Certification requirements impact

---

## Quality Checklist

**Before delivery:**
- [ ] All findings validated and reproducible
- [ ] Evidence complete and clear
- [ ] Remediation actionable and specific
- [ ] Executive summary non-technical
- [ ] No client data exposed in examples
- [ ] Professional formatting throughout
- [ ] CVSS scores justified
- [ ] Spelling/grammar checked
- [ ] File paths sanitized (no personal info)
- [ ] Report sanitized for distribution

---

**See Also:**
- `skills/security-testing/templates/PENTEST-REPORT-TEMPLATE.md` - Complete template
- `skills/security-testing/templates/FINDING-TEMPLATE.md` - Individual finding format
- `skills/security-testing/reference/SCOPE-COMPLIANCE-GUIDE.md` - Compliance standards
