# Dual-Model QA Review Methodology

**Purpose:** Reduce hallucinations and blind spots through parallel structured and adversarial review

**Models:** Latest Haiku (structured) + Latest Grok (adversarial)

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` automatically selects latest model versions via OpenRouter API

---

## Overview

The dual-model approach combines two complementary review perspectives:

1. **Haiku Structured Review** - Fast, checklist-based validation focusing on completeness, accuracy, and standards compliance
2. **Grok Adversarial Review** - Challenge assumptions, identify logical gaps, and surface potential hallucinations
3. **Cross-Validation** - Compare outputs to find conflicts, calculate confidence levels, and prioritize issues

**Benefits:**
- Reduces hallucinations (dual verification)
- Catches blind spots (different model perspectives)
- Increases confidence (agreement = high confidence)
- Maintains efficiency (Haiku fast, Grok targeted)

---

## Phase 1: Haiku Structured Review (Efficiency)

**Purpose:** Systematic validation against checklists and standards

**Focus Areas:**

### Completeness Validation
- All required sections present
- Supporting evidence included (screenshots, logs, scan outputs)
- References and citations complete
- Methodology documented
- Remediation guidance provided

**Checklist:**
```
- [ ] Executive summary present (2-3 pages, non-technical)
- [ ] Scope and objectives documented
- [ ] Methodology section included (framework referenced)
- [ ] All findings numbered and titled
- [ ] Evidence attachments present (screenshots, logs)
- [ ] Remediation guidance actionable
- [ ] References and citations complete
```

### Standards Compliance
- PTES (penetration testing)
- OWASP ASVS/WSTG (web application security)
- NIST SP 800-115 (technical testing)
- IEEE 1028 (review process)
- ISO/IEC 20246 (work product reviews)

**Validation:**
- Verify framework adherence (PTES methodology followed)
- Check section completeness (all required sections present)
- Validate compliance with client requirements

### Technical Accuracy
- CVSS v3.1 scores calculated correctly
- CVE/CWE mappings accurate
- Reproduction steps tested and verified
- Evidence supports claims (screenshots match descriptions)
- Technical details precise (IP addresses, ports, protocols)

**Validation Process:**
```
For each finding:
1. Verify CVSS score calculation (use CVSS calculator)
2. Check CVE/CWE mapping (reference MITRE/NVD)
3. Test reproduction steps (can it be replicated?)
4. Match evidence to claim (screenshot shows described issue?)
5. Validate technical details (correct syntax, accurate data)
```

### Consistency Checks
- Terminology uniform throughout
- Severity ratings aligned (Critical = CVSS 9.0-10.0)
- Formatting standardized (headings, lists, code blocks)
- Cross-references valid (all internal links work)

**Common Issues:**
- Inconsistent severity labels (Critical vs CRITICAL vs critical)
- Variable terminology (same concept, different terms)
- Formatting drift (early sections formatted, later sections not)
- Broken references (Figure 12 mentioned but missing)

### Citation Validation
- All external references have working URLs
- Citations formatted correctly
- Source reliability verified
- Publication dates included

### Grammar and Style
- Active voice preferred
- Present tense used
- Inclusive language (no gendered terms)
- Technical jargon explained
- Consistent terminology

**HAIKU OUTPUT:**
```markdown
# Haiku Structured Review

## Completeness: PASS/FAIL
- [List missing sections or confirmed complete]

## Standards Compliance: PASS/FAIL
- [Framework adherence, required sections]

## Technical Accuracy: X issues found
- ISSUE-001: [Description with line number]
- ISSUE-002: [Description with line number]

## Consistency: X issues found
- [Terminology, formatting, cross-reference issues]

## Citations: X issues found
- [Broken links, missing sources]

## Grammar/Style: X issues found
- [Active voice, tense, clarity issues]

## Overall Rating: [1-5 scale]
1 = Major revisions required
2 = Significant issues
3 = Moderate issues
4 = Minor issues
5 = Excellent quality
```

---

## Phase 2: Grok Adversarial Review (Challenge)

**Purpose:** Challenge assumptions, identify overstatements, surface hallucinations

**Focus Areas:**

### Question Assumptions
- Are conclusions supported by evidence?
- Are risk ratings justified?
- Are impact claims realistic?
- Are likelihood estimates accurate?

**Example:**
```
CLAIM: "This vulnerability allows complete system compromise"
QUESTION: Evidence shows web shell upload, but does it demonstrate privilege escalation to root? Is "complete compromise" overstated?
```

### Identify Logical Fallacies
- Correlation vs causation confusion
- False dichotomies (only two options presented)
- Hasty generalizations (small sample, broad claim)
- Appeal to authority without evidence

### Check for Overstatement
- "All endpoints vulnerable" - Were all endpoints tested?
- "Critical business impact" - Is this demonstrated or assumed?
- "Immediate exploitation" - Is active exploitation confirmed?
- "APT group attribution" - Is there concrete evidence?

### Validate Evidence-to-Claim Alignment
- Does the evidence support the strength of the claim?
- Are screenshots sufficient or is additional proof needed?
- Do HTTP logs demonstrate the described behavior?
- Are proof-of-concept outputs complete?

**Evidence Strength Scale:**
```
Strong: Multiple independent sources, reproducible steps, complete logs
Moderate: Single source, reproducible steps, partial logs
Weak: Single screenshot, no reproduction steps, missing context
Insufficient: Claim without supporting evidence
```

### Surface Potential Hallucinations
- Fabricated CVE IDs (verify CVE exists)
- Incorrect tool outputs (does Nmap output match claim?)
- Misattributed vulnerabilities (is this the right CWE?)
- Speculative conclusions (fact vs hypothesis)

### Identify Missing Edge Cases
- What if authentication is enabled?
- What if rate limiting is present?
- What if input validation is improved?
- What about alternative attack vectors?

### Challenge Risk Ratings
- Is CVSS scoring justified?
- Is likelihood assessment realistic?
- Is business impact overstated?
- Are mitigating factors considered?

**GROK OUTPUT:**
```markdown
# Grok Adversarial Review

## Assumptions Challenged: X items
- CHALLENGE-001: [Finding ID] - [Assumption + Question]
- CHALLENGE-002: [Finding ID] - [Assumption + Question]

## Logical Gaps: X items
- GAP-001: [Description of logical inconsistency]

## Overstatements: X items
- OVERSTATE-001: [Claim + Evidence mismatch]

## Evidence Sufficiency: X items
- INSUFFICIENT-001: [Finding ID] - [Missing evidence]

## Potential Hallucinations: X items
- HALLUCINATION-001: [Fabricated data or incorrect reference]

## Missing Edge Cases: X items
- EDGE-001: [Scenario not considered]

## Risk Rating Challenges: X items
- RISK-001: [Finding ID] - [Rating + Justification question]

## Overall Confidence: [1-5 scale]
1 = Major concerns, significant revision needed
2 = Multiple challenges, evidence gaps
3 = Some concerns, minor gaps
4 = Minor challenges, mostly sound
5 = High confidence, well-supported
```

---

## Phase 3: Cross-Validation

**Purpose:** Compare Haiku and Grok outputs to identify high-confidence issues and conflicts

### Agreement Matrix

**Both Models Agree = HIGH Confidence**
- If both Haiku and Grok flag the same issue, it's likely valid
- Prioritize these for immediate remediation

**Example:**
```
Haiku: "VULN-003 CVSS score incorrect (should be 8.1, not 9.0)"
Grok: "VULN-003 risk rating overstated, CVSS calculation error detected"
RESULT: HIGH confidence - Fix CVSS score
```

**Only One Model Flags = MEDIUM Confidence**
- If only Haiku or Grok finds an issue, manual review needed
- May be valid but requires human judgment

**Example:**
```
Haiku: "Inconsistent severity labels (Critical vs CRITICAL)"
Grok: [No mention]
RESULT: MEDIUM confidence - Likely formatting issue, low priority
```

### Conflict Resolution

**Models Disagree = Flag for Manual Review**
- Different perspectives on same finding
- Requires human expertise to resolve

**Example:**
```
Haiku: "VULN-005 remediation guidance actionable and clear"
Grok: "VULN-005 remediation may break legitimate functionality"
RESULT: CONFLICT - Manual review required
```

### Confidence Levels

**Calculate confidence based on agreement:**
```
HIGH (90-100%): Both models agree on issue + severity
MEDIUM (60-89%): Both models identify issue, different severity
LOW (30-59%): Only one model flags issue
VERY LOW (<30%): Models contradict each other
```

### Gap Identification

**Issues Missed by Both Models**
- Review areas where neither model flagged concerns
- May indicate blind spots in methodology
- Consider manual spot-checking

**CROSS-VALIDATION OUTPUT:**
```markdown
# Cross-Validation Report

## High-Confidence Issues (Both Agree)
- ISSUE-001: [Description] - Haiku + Grok both flagged
- ISSUE-002: [Description] - Haiku + Grok both flagged

## Medium-Confidence Issues (Single Model)
- ISSUE-003: [Description] - Haiku only
- ISSUE-004: [Description] - Grok only

## Conflicts (Manual Review Required)
- CONFLICT-001: [Description] - Haiku says X, Grok says Y
- CONFLICT-002: [Description] - Haiku says X, Grok says Y

## Potential Blind Spots
- [Areas where neither model flagged concerns]

## Priority Ranking
1. High-confidence issues (immediate action)
2. Conflicts (manual review)
3. Medium-confidence issues (verify)
4. Low-priority formatting/style issues
```

---

## Quality Criteria Validation

**All reviews validate against these criteria:**

### 1. Completeness
- All required sections present
- Supporting evidence included
- References complete
- Methodology documented

### 2. Accuracy
- Technical details verified
- CVSS scores validated
- CVE/CWE mappings correct
- Evidence supports claims

### 3. Consistency
- Terminology uniform
- Severity ratings aligned
- Formatting standardized
- Cross-references valid

### 4. Clarity
- Executive summary understandable (non-technical audience)
- Technical findings detailed (reproducible by peer)
- Remediation guidance actionable (specific steps)
- Risk context provided (business impact)

### 5. Compliance
- Follows applicable standard (PTES, OWASP, NIST)
- Meets client requirements
- Adheres to professional ethics
- Respects confidentiality

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

**Version:** 2.0
**Framework:** ISO/IEC 20246 + IEEE 1028
**Models:** Latest Haiku (structured) + Latest Grok (adversarial)
**Selection:** OpenRouter API dynamic model discovery
