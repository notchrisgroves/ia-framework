---
name: qa-review
description: Support skill providing dual-model peer review methodology (Haiku + Grok) for other skills. Not standalone - always invoked with caller context and review target.
---

# QA Review Skill (Support Skill)

**Support skill loaded by: writer, security-testing, security-advisory, code-review**

Provides QA review methodology (dual-model validation, standards compliance, hallucination detection) for skills that need quality assurance.

**Core Philosophy:** Multi-model validation reduces errors. Haiku provides structured compliance checking, Grok challenges assumptions. This skill provides HOW to review - calling skills define WHAT to review.

---

## 🚨 Critical Rules

**This is a SUPPORT SKILL - not standalone:**

1. **Always Called with Context** - Caller provides: review target, review type, output location, depth level
2. **Dual-Model Review Required** - Always use Haiku (structured) + Grok (adversarial), never single-model
3. **Evidence-Based Findings Only** - All critique needs specific line numbers, sections, or evidence (no generic feedback)
4. **Standards Compliance Mandatory** - Validate against applicable standards (PTES, OWASP, NIST, IEEE)
5. **Caller-Specific Output** - Return findings to caller's specified directory

**Quality Standards = Professional Credibility** - See `reference/standards.md`

---

## Support Skill Architecture

**How delegation works:**

```
Calling Skill → Defines WHAT to review → qa-review executes HOW

Example:
  writer needs: "Blog post QA with ≥4 rating before publishing"
  qa-review executes: Dual-model methodology, returns rating + findings
```

**Caller Context Required:**
- **Calling skill:** Who invoked qa-review (writer, security-testing, etc.)
- **Review target:** What to review (blog post, pentest report, code review findings)
- **Review type:** peer-review or hallucination-detection
- **Depth level:** quick/standard/deep
- **Output location:** Where to save QA findings

---

## Decision Tree: Caller Detection

**Level 1: Who is calling this skill?**

### Caller 1: writer

**Context:** Blog post and documentation quality assurance before publishing

**Review Plan (from caller):**
- Technical accuracy verification
- Citation and URL validation
- Evidence-to-claim alignment
- SEO and readability checks
- Intelligence Adjacent voice consistency
- Rating requirement: ≥4 to publish

**Depth Level:** Standard (comprehensive review)

**Output:** `blog/{slug}/qa-review.json`

**Methodology:** Dual-model (Haiku structure + Grok adversarial) with rating system

---

### Caller 2: security-testing

**Context:** Pentest report validation before client delivery

**Review Plan (from caller):**
- Standards compliance (PTES, OWASP)
- CVSS scoring accuracy
- CVE/CWE verification (valid IDs)
- Evidence sufficiency for findings
- Remediation guidance clarity
- Executive summary effectiveness

**Depth Level:** Deep (client-facing deliverable)

**Output:** `output/engagements/pentest/{target}/qa-review/`

**Methodology:** Dual-model with ISO/IEC 20246 technical review standards

---

### Caller 3: security-advisory

**Context:** Risk assessment and advisory report quality check

**Review Plan (from caller):**
- Risk rating justification
- Control recommendations accuracy
- Compliance framework alignment (HIPAA, PCI-DSS, etc.)
- Client communication clarity
- Actionable remediation guidance

**Depth Level:** Standard

**Output:** `output/engagements/advisory/{client}/qa-review/`

**Methodology:** Dual-model with NIST SP 800-53A assessment standards

---

### Caller 4: code-review

**Context:** Code review findings validation

**Review Plan (from caller):**
- Vulnerability classification accuracy (CWE mapping)
- Severity rating justification
- Remediation code samples accuracy
- False positive identification
- Coverage completeness

**Depth Level:** Quick to Standard (depending on findings count)

**Output:** `output/engagements/code-review/{project}/qa-review/`

**Methodology:** Dual-model with OWASP Code Review Guide standards

---

## Review Types

**All callers can request either:**

### Type 1: Peer Review (Default)

**Characteristics:**
- 6-phase process (Preparation, Haiku Review, Grok Review, Cross-Validation, Manual Decision, Reporting)
- Checklist-based validation (completeness, correctness, consistency, clarity, compliance)
- Standards compliance verification
- Dual-model validation
- Evidence-based feedback with line numbers
- 2-6 hours duration

**Use when:** Comprehensive quality assurance needed before delivery

**Workflow:** `workflows/qa-review-workflow.md`

---

### Type 2: Hallucination Detection (Fast)

**Characteristics:**
- Grok adversarial review emphasized
- Factual verification priority (CVE/CWE validation, URL checking)
- Citation discipline enforcement
- Evidence provenance tracking
- Quick turnaround (1-2 hours)

**Use when:** AI-generated content needs factual verification

**Workflow:** `workflows/hallucination-detection.md`

---

## Delegation Examples

**See:** `reference/delegation-examples.md` for complete caller context examples

**Quick reference - delegation block format:**
```markdown
**DELEGATE to qa-review skill:**
**Caller:** [skill-name]
**Review Type:** peer-review | hallucination-detection
**Review Target:** [file/directory path]
**Depth Level:** quick | standard | deep
**Requirements:** [caller-specific criteria]
**Output:** [caller's output directory]
```

---

## Workflow: Peer Review (6 Phases)

**PREPARE → HAIKU_REVIEW → GROK_REVIEW → CROSS_VALIDATE → MANUAL_DECISION → REPORT**

| Phase | Duration | Key Activities | Output |
|-------|----------|----------------|--------|
| 1. Preparation | 30-60 min | Identify target, gather materials, define criteria | Review plan |
| 2. Haiku Review | 30-90 min | Checklist validation, standards compliance, accuracy | Haiku report |
| 3. Grok Review | 30-60 min | Challenge assumptions, detect overstatements, find gaps | Grok report |
| 4. Cross-Validation | 30-45 min | Compare findings, calculate confidence, flag conflicts | Agreement matrix |
| 5. Manual Decision | 30-60 min | Resolve conflicts, validate medium-confidence issues | Decision log |
| 6. Reporting | 30-45 min | Consolidate findings, categorize severity, remediation | Final QA report |

**Confidence Levels:** High (both agree) | Medium (one flagged) | Low (conflict)

**Complete workflow:** `workflows/qa-review-workflow.md`

---

## Workflow: Hallucination Detection

**VERIFY → CHALLENGE → FLAG → REPORT**

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| 1. Verify | Factual | CVE/CWE IDs in NVD/MITRE, URL validation |
| 2. Challenge | Adversarial | Grok challenges claims, evidence-to-claim alignment |
| 3. Flag | Categorize | Hallucinations, unsupported claims, incorrect refs |
| 4. Report | Deliverable | Corrections needed, evidence gaps |

**Complete workflow:** `workflows/hallucination-detection.md`

---

## Dual-Model Review Methodology

| Model | Role | Focus Areas |
|-------|------|-------------|
| **Haiku** | Structured | Checklists, standards (PTES/OWASP/NIST), completeness, accuracy |
| **Grok** | Adversarial | Challenge assumptions, detect overstatements, find hallucinations |

**Cross-Validation:** Compare outputs → Calculate confidence → Flag conflicts → Prioritize by severity

**Complete methodology:** `methodologies/dual-model-review.md`

---

## Quality Criteria (5 Dimensions)

**All reviews validate against:**

1. **Completeness** - All required sections present, supporting evidence included, references complete
2. **Correctness** - Technical details accurate, claims supported, calculations verified
3. **Consistency** - Terminology uniform, severity ratings aligned, formatting standardized
4. **Clarity** - Executive summary understandable, technical findings detailed, remediation actionable
5. **Compliance** - Follows applicable standards, meets client requirements, adheres to ethics

**See:** `reference/quality-criteria.md` for detailed checklists

---

## Standards and Frameworks

**Primary Standards:**
- **ISO/IEC 20246:2017** - Work product review process
- **IEEE 1028:2008** - Software reviews and audits

**Supporting Standards:**
- **OWASP Code Review Guide** - Security-focused review criteria
- **Google Engineering Practices** - Efficient review guidelines
- **NIST SP 800-53A** - Security control assessment procedures

**Review Types (ISO/IEC 20246):**
- Management Review (business alignment, progress)
- Technical Review (technical accuracy, completeness)
- Inspection (formal defect detection)
- Walkthrough (knowledge sharing)
- Audit (compliance verification)

**See:** `reference/standards.md` for complete standards documentation

---

## Output Structure

**Caller-specific output locations:**

```
# writer
blog/{slug}/
   qa-review.json                     (Rating + findings)

# security-testing
output/engagements/pentest/{target}/qa-review/
   README.md                          (Review objectives)
   SESSION-STATE.md                   (Session tracking)
   01-source-materials/
   02-haiku-review/
   03-grok-review/
   04-cross-validation/
   05-manual-review/
   06-final-report/
      qa-review-final-report.md

# security-advisory
output/engagements/advisory/{client}/qa-review/
   [Same structure as security-testing]

# code-review
output/engagements/code-review/{project}/qa-review/
   [Same structure as security-testing]
```

---

## Safety Guardrails

**Hallucination Detection:**
- Both models flag unsupported claims
- Require citations for all assertions
- Validate evidence-to-claim alignment
- Clearly distinguish fact vs hypothesis

**Professional Standards:**
- Follow ISO/IEC 20246 review processes
- Maintain objectivity and fairness
- Respect work product confidentiality
- Provide constructive feedback

**Quality Assurance:**
- Multi-model validation reduces errors
- Human oversight for final decisions
- Document all review findings
- Track remediation status

---

## Session Checkpoint Protocol

**Checkpoint triggers:**
- After each review phase completion (Haiku, Grok, Cross-Validation, Manual Decision)
- Every 2 hours during long reviews
- When switching between different work products
- User explicitly requests checkpoint

**SESSION-STATE.md format:**
```yaml
skill: qa-review
session_number: [N]
phase: [preparation/haiku-review/grok-review/cross-validation/manual-decision/reporting]
status: [in-progress/completed]

# Review metadata
review_target: [pentest-report/code-review/documentation]
review_type: [management/technical/inspection/walkthrough/audit]
review_depth: [quick/standard/deep]

# Phase-specific tracking
haiku_rating: [1-5 scale]
grok_confidence: [1-5 scale]
critical_issues: [count]
high_issues: [count]
medium_issues: [count]
low_issues: [count]
conflicts_flagged: [count]

# Files created
files_created:
  - [list of reports generated]

# Next actions
next_action: [what to do next]
timestamp: [YYYY-MM-DD HH:MM]
```

**See:** `docs/session-checkpoint-enforcement.md` for complete protocol

---

## Tools

| Tool | Purpose | Location |
|------|---------|----------|
| Haiku | Structured review | `tools/openrouter/` |
| Grok | Adversarial review | `tools/openrouter/` |
| Read | Source material access | Native |
| Write | Report generation | Native |

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `standards.md` | ISO/IEC 20246, IEEE 1028 compliance |
| `quality-criteria.md` | 5 dimensions checklist |
| `dual-model-review.md` | Haiku + Grok methodology |
| `review-checklist.md` | All review type checklists |

---

## Integration Points

**Security Testing Integration:**
- Review pentest reports before client delivery
- Validate vulnerability scanner outputs
- QA architecture review findings

**Personal Development Integration:**
- Review resume content for accuracy
- Validate job application materials

**Writer Integration:**
- Review blog posts for technical accuracy
- QA technical documentation
- Validate security reports before publication

---

## Common Scenarios

**Peer Review:** "Review pentest report before delivery"
→ Peer Review → 6 phases → Dual-model → 2-6 hours

**Hallucination Detection:** "Check AI-generated report for hallucinations"
→ Hallucination Detection → Grok focus → Factual verification → 1-2 hours

**Quick QA:** "Quick quality check on technical docs"
→ Peer Review → Quick depth → 2-4 hours

---

## Version History

**v3.0 (2025-12-17)** - Support skill pattern (delegated by other skills, caller context detection)
- Caller detection router (writer, security-testing, security-advisory, code-review)
- Delegation examples with caller context
- Caller-specific output locations
- Support skill architecture (HOW to review, callers define WHAT)

**v2.0 (2025-12-11)** - Fresh framework rebuild
- Decision tree router (Peer Review vs Hallucination Detection)
- Dual-model methodology (Haiku + Grok)
- 6-phase workflow with checkpoints
- Progressive disclosure architecture

---

**Version:** 3.0
**Last Updated:** 2025-12-17
**Status:** Support skill (delegated by other skills, caller context detection)
