# QA Review Delegation Examples

**Purpose:** Complete delegation examples for skills calling qa-review

---

## Example 1: writer → qa-review

**Caller context:**
```markdown
# From writer/workflows/blog-content.md

### Stage 3: QA REVIEW (MANDATORY GATE)

**DELEGATE to qa-review skill:**

**Caller:** writer
**Review Type:** peer-review
**Review Target:** output/blog/drafts/{slug}/draft.md
**Depth Level:** standard
**Requirements:**
  - Technical accuracy verification
  - Citation validation (all URLs working)
  - Evidence-to-claim alignment
  - SEO and readability
  - Rating requirement: ≥4 to publish

**Output:** output/blog/drafts/{slug}/qa-review.json

qa-review executes dual-model methodology and returns rating + findings.
```

---

## Example 2: security-testing → qa-review

**Caller context:**
```markdown
# From security-testing/workflows/pentest-delivery.md

### Phase 5: QA Validation

**DELEGATE to qa-review skill:**

**Caller:** security-testing
**Review Type:** peer-review
**Review Target:** output/engagements/pentest/{target}/report/final-report.md
**Depth Level:** deep
**Requirements:**
  - PTES/OWASP standards compliance
  - CVSS scoring accuracy
  - CVE/CWE ID verification
  - Evidence sufficiency
  - Client communication clarity

**Output:** output/engagements/pentest/{target}/qa-review/

qa-review executes ISO/IEC 20246 technical review standards.
```

---

## Example 3: security-advisory → qa-review

**Caller context:**
```markdown
# From security-advisory/workflows/risk-assessment.md

### Phase 6: Report QA

**DELEGATE to qa-review skill:**

**Caller:** security-advisory
**Review Type:** peer-review
**Review Target:** output/engagements/advisory/{client}/risk-assessment-report.md
**Depth Level:** standard
**Requirements:**
  - Risk rating justification
  - Control recommendations accuracy
  - Compliance alignment (HIPAA, PCI-DSS, etc.)
  - Actionable remediation guidance

**Output:** output/engagements/advisory/{client}/qa-review/

qa-review executes NIST SP 800-53A assessment standards.
```

---

## Example 4: code-review → qa-review

**Caller context:**
```markdown
# From code-review/workflows/security-code-review.md

### Phase 4: Findings QA

**DELEGATE to qa-review skill:**

**Caller:** code-review
**Review Type:** peer-review
**Review Target:** output/engagements/code-review/{project}/findings/
**Depth Level:** standard
**Requirements:**
  - CWE classification accuracy
  - Severity rating justification
  - Remediation code samples accuracy
  - False positive check

**Output:** output/engagements/code-review/{project}/qa-review/

qa-review executes OWASP Code Review Guide standards.
```

---

**Created:** 2025-12-18
**Purpose:** Complete delegation examples extracted from SKILL.md for line count compliance
